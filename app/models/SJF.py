from .process import Process

def sjf_scheduling(processes):
    """
    Shortest Job First Scheduling (Non-Preemptive).
    This function schedules processes based on their burst time, prioritizing the shortest burst time first.
    It calculates and returns the waiting time, turnaround time, and completion time for each process,
    along with the average waiting and turnaround times.
    """
    # Sort processes by arrival time initially
    processes.sort(key=lambda p: p.arrival_time)
    n = len(processes)  # Total number of processes
    completed = 0  # Counter for completed processes
    current_time = 0  # Tracks the current time in the scheduling
    total_waiting = 0  # Accumulates total waiting time
    total_turnaround = 0  # Accumulates total turnaround time
    done = [False] * n  # Tracks whether each process is completed

    while completed < n:
        idx = -1  # Index of the process to execute next
        min_burst = float('inf')  # Minimum burst time found in the current iteration

        # Find the process with the shortest burst time that has arrived
        for i, p in enumerate(processes):
            if p.arrival_time <= current_time and not done[i]:  # Process has arrived and is not completed
                if p.burst_time < min_burst:  # Check if this process has the shortest burst time
                    min_burst = p.burst_time
                    idx = i

        if idx == -1:  # No process is ready yet
            # Advance time to the next process's arrival time
            current_time = min(p.arrival_time for i, p in enumerate(processes) if not done[i])
            continue

        # Process the selected process
        p = processes[idx]
        p.completion_time = current_time + p.burst_time  # Calculate completion time
        p.turnaround_time = p.completion_time - p.arrival_time  # Calculate turnaround time
        p.waiting_time = p.turnaround_time - p.burst_time  # Calculate waiting time

        # Update current time and totals
        current_time = p.completion_time
        total_waiting += p.waiting_time
        total_turnaround += p.turnaround_time
        done[idx] = True  # Mark the process as completed
        completed += 1  # Increment the completed process count

    # Prepare the rows for display with process details
    rows = [{
        'process': p.name,
        'arrival': p.arrival_time,
        'burst': p.burst_time,
        'priority': p.priority,
        'waiting': p.waiting_time,
        'turnaround': p.turnaround_time,
        'completion': p.completion_time
    } for p in processes]

    # Calculate average waiting and turnaround times
    avg_waiting = total_waiting / n
    avg_turnaround = total_turnaround / n

    # Return the results as a dictionary
    return {
        'rows': rows,
        'avg_waiting_time': avg_waiting,
        'avg_turnaround_time': avg_turnaround
    }
