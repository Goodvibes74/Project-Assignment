from .process import Process

def fcfs_scheduling(processes):
    """
    First-Come, First-Served Scheduling.
    Expects 'processes' as a list of Process objects.
    """
    if not processes:
        # Return early if there are no processes
        return {
            'rows': [],
            'avg_waiting_time': 0,
            'avg_turnaround_time': 0
        }

    # Sort by arrival time
    processes.sort(key=lambda p: p.arrival_time)
    current_time = 0
    total_waiting = 0
    total_turnaround = 0

    for p in processes:
        # Debugging print to check the process values
        print(f"Processing: {p.name}, Arrival Time: {p.arrival_time}, Burst Time: {p.burst_time}")

        if p.arrival_time > current_time:
            current_time = p.arrival_time
        
        # Calculate completion time, turnaround time, and waiting time
        p.completion_time = current_time + p.burst_time
        p.turnaround_time = p.completion_time - p.arrival_time
        p.waiting_time = p.turnaround_time - p.burst_time

        current_time = p.completion_time
        total_waiting += p.waiting_time
        total_turnaround += p.turnaround_time

    # Prepare data for display
    rows = [{
        'process': p.name,
        'arrival': p.arrival_time,
        'burst': p.burst_time,
        'priority': p.priority,
        'waiting': p.waiting_time,
        'turnaround': p.turnaround_time,
        'completion': p.completion_time
    } for p in processes]

    # Debugging print to check if rows are populated correctly
    print(f"Rows: {rows}")

    # Avoid division by zero if the list is empty
    avg_waiting = total_waiting / len(processes) if len(processes) > 0 else 0
    avg_turnaround = total_turnaround / len(processes) if len(processes) > 0 else 0

    # Return result data to be passed to the template
    return {
        'rows': rows,
        'avg_waiting_time': avg_waiting,
        'avg_turnaround_time': avg_turnaround
    }
