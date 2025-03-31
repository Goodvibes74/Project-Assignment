# app/models/Round_Robin.py
from collections import deque
from models.process import Process

def round_robin_scheduling(processes, quantum):
    """
    Round Robin Scheduling Algorithm.
    This function simulates the Round Robin CPU scheduling algorithm.
    
    Args:
        processes (list): List of Process objects, each representing a process.
        quantum (int): Time quantum for the Round Robin scheduling.

    Returns:
        dict: A dictionary containing:
            - 'rows': List of dictionaries with process details (name, arrival, burst, etc.).
            - 'avg_waiting_time': Average waiting time of all processes.
            - 'avg_turnaround_time': Average turnaround time of all processes.
    """
    # Sort processes by their arrival time.
    processes.sort(key=lambda p: p.arrival_time)
    n = len(processes)  # Total number of processes
    current_time = 0  # Tracks the current time in the simulation
    total_waiting = 0  # Total waiting time for all processes
    total_turnaround = 0  # Total turnaround time for all processes
    completed = 0  # Number of processes that have completed execution
    ready_queue = deque()  # Queue to hold processes ready for execution
    i = 0  # Index to track processes that have arrived

    while completed < n:
        # Add processes that have arrived to the ready queue.
        while i < n and processes[i].arrival_time <= current_time:
            ready_queue.append(processes[i])
            i += 1

        if not ready_queue:
            # If the ready queue is empty, jump to the next process arrival time.
            current_time = processes[i].arrival_time
            ready_queue.append(processes[i])
            i += 1

        # Get the next process from the ready queue.
        current_process = ready_queue.popleft()
        # Determine the time the process will run in this quantum.
        run_time = min(quantum, current_process.remaining_time)
        current_process.remaining_time -= run_time
        current_time += run_time

        # Add any new arrivals during this quantum to the ready queue.
        while i < n and processes[i].arrival_time <= current_time:
            ready_queue.append(processes[i])
            i += 1

        if current_process.remaining_time == 0:
            # If the process has completed execution, calculate its metrics.
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            total_waiting += current_process.waiting_time
            total_turnaround += current_process.turnaround_time
            completed += 1
        else:
            # If the process is not finished, add it back to the ready queue.
            ready_queue.append(current_process)

    # Prepare the results for each process.
    rows = [{
        'process': p.name,
        'arrival': p.arrival_time,
        'burst': p.burst_time,
        'priority': p.priority,
        'waiting': p.waiting_time,
        'turnaround': p.turnaround_time,
        'completion': p.completion_time
    } for p in processes]

    # Calculate average waiting and turnaround times.
    avg_waiting = total_waiting / n
    avg_turnaround = total_turnaround / n

    # Return the results as a dictionary.
    return {
        'rows': rows,
        'avg_waiting_time': avg_waiting,
        'avg_turnaround_time': avg_turnaround
    }
