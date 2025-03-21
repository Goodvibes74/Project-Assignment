# app/models/FCFS.py
from .process import Process

def fcfs_scheduling(processes):
    """
    First-Come, First-Served Scheduling.
    Expects 'processes' as a list of Process objects.
    """
    # Sort by arrival time
    processes.sort(key=lambda p: p.arrival_time)
    current_time = 0
    total_waiting = 0
    total_turnaround = 0

    for p in processes:
        if p.arrival_time > current_time:
            current_time = p.arrival_time
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

    avg_waiting = total_waiting / len(processes)
    avg_turnaround = total_turnaround / len(processes)
    return {
        'rows': rows,
        'avg_waiting_time': avg_waiting,
        'avg_turnaround_time': avg_turnaround
    }
