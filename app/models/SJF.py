from .process import Process

def sjf_scheduling(processes):
    """
    Shortest Job First Scheduling (Non-Preemptive).
    """
    # Sort processes by arrival time initially
    processes.sort(key=lambda p: p.arrival_time)
    n = len(processes)
    completed = 0
    current_time = 0
    total_waiting = 0
    total_turnaround = 0
    done = [False] * n

    while completed < n:
        idx = -1
        min_burst = float('inf')
        # Find the process with the shortest burst time that has arrived
        for i, p in enumerate(processes):
            if p.arrival_time <= current_time and not done[i]:
                if p.burst_time < min_burst:
                    min_burst = p.burst_time
                    idx = i

        if idx == -1:  # No process is ready yet
            current_time = min(p.arrival_time for i, p in enumerate(processes) if not done[i])
            continue

        p = processes[idx]
        p.completion_time = current_time + p.burst_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

        current_time = p.completion_time
        total_waiting += p.waiting_time
        total_turnaround += p.turnaround_time
        done[idx] = True
        completed += 1

    # Prepare the rows for display
    rows = [{
        'process': p.name,
        'arrival': p.arrival_time,
        'burst': p.burst_time,
        'priority': p.priority,
        'waiting': p.waiting_time,
        'turnaround': p.turnaround_time,
        'completion': p.completion_time
    } for p in processes]

    avg_waiting = total_waiting / n
    avg_turnaround = total_turnaround / n

    return {
        'rows': rows,
        'avg_waiting_time': avg_waiting,
        'avg_turnaround_time': avg_turnaround
    }
