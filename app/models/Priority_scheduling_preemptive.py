# app/models/Priority_scheduling_preemptive.py
from .process import Process

def priority_preemptive_scheduling(processes):
    """
    Priority Scheduling (Preemptive).
    Lower priority value means higher priority.
    """
    processes.sort(key=lambda p: p.arrival_time)
    n = len(processes)
    current_time = 0
    completed = 0
    total_waiting = 0
    total_turnaround = 0

    while completed < n:
        ready = [p for p in processes if p.arrival_time <= current_time and p.remaining_time > 0]
        if not ready:
            current_time = min([p.arrival_time for p in processes if p.remaining_time > 0])
            continue

        current_process = min(ready, key=lambda p: p.priority)
        current_process.remaining_time -= 1
        current_time += 1

        if current_process.remaining_time == 0:
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            total_waiting += current_process.waiting_time
            total_turnaround += current_process.turnaround_time
            completed += 1

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
