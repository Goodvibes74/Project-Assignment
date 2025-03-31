# app/models/SJF_preemptive.py
from .process import Process

def sjf_preemptive_scheduling(processes):
    """
    Shortest Remaining Time First (Preemptive SJF) Scheduling Algorithm.
    This function schedules processes based on the shortest remaining time.
    It calculates waiting time, turnaround time, and completion time for each process.
    """

    # Sort processes by their arrival time
    processes.sort(key=lambda p: p.arrival_time)
    n = len(processes)  # Total number of processes
    current_time = 0  # Tracks the current time in the scheduling process
    completed = 0  # Number of processes completed
    total_waiting = 0  # Total waiting time for all processes
    total_turnaround = 0  # Total turnaround time for all processes

    # Loop until all processes are completed
    while completed < n:
        # Get all processes that have arrived and are not yet completed
        ready = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
        
        # If no process is ready, move to the next earliest arrival time
        if not ready:
            current_time = min([p.arrival_time for p in processes if p.remaining_time > 0])
            continue

        # Select the process with the shortest remaining time
        current_process = min(ready, key=lambda p: p.remaining_time)
        
        # Execute the selected process for one unit of time
        current_process.remaining_time -= 1
        current_time += 1

        # If the process is completed, calculate its metrics
        if current_process.remaining_time == 0:
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            total_waiting += current_process.waiting_time
            total_turnaround += current_process.turnaround_time
            completed += 1

    # Prepare the result rows with process details
    rows = [{
        'process': p.name,
        'arrival': p.arrival_time,
        'burst': p.burst_time,
        'priority': p.priority,
        'waiting': p.waiting_time,
        'turnaround': p.turnaround_time,
        'completion': p.completion_time
    } for p in processes]

    # Calculate average waiting time and turnaround time
    avg_waiting = total_waiting / n
    avg_turnaround = total_turnaround / n

    # Return the results as a dictionary
    return {
        'rows': rows,
        'avg_waiting_time': avg_waiting,
        'avg_turnaround_time': avg_turnaround
    }
