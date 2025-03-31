# app/models/Priority_scheduling.py
from .process import Process

def priority_scheduling(processes):
    """
    Priority Scheduling (Non-Preemptive).
    Lower priority value means higher priority.
    """
    # Sort processes by their arrival time
    processes.sort(key=lambda p: p.arrival_time)
    n = len(processes)  # Total number of processes
    completed = 0  # Counter for completed processes
    current_time = 0  # Tracks the current time in the scheduling
    total_waiting = 0  # Total waiting time for all processes
    total_turnaround = 0  # Total turnaround time for all processes
    done = [False] * n  # Tracks whether a process is completed

    # Loop until all processes are completed
    while completed < n:
        idx = -1  # Index of the process to execute next
        best_priority = float('inf')  # Initialize with the highest possible priority value

        # Find the process with the highest priority (lowest priority value) that has arrived
        for i, p in enumerate(processes):
            if p.arrival_time <= current_time and not done[i]:
                if p.priority < best_priority:
                    best_priority = p.priority
                    idx = i

        # If no process is ready, move to the next earliest arrival time
        if idx == -1:
            current_time = min([p.arrival_time for i, p in enumerate(processes) if not done[i]])
            continue

        # Execute the selected process
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

    # Prepare the result rows for each process
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
