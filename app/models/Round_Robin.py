# app/models/Round_Robin.py
from collections import deque
from models.process import Process

def round_robin_scheduling(processes, quantum):
    """
    Round Robin Scheduling.
    """
    processes.sort(key=lambda p: p.arrival_time)
    n = len(processes)
    current_time = 0
    total_waiting = 0
    total_turnaround = 0
    completed = 0
    ready_queue = deque()
    i = 0  # index for processes

    while completed < n:
        # Add processes that have arrived to the ready queue.
        while i < n and processes[i].arrival_time <= current_time:
            ready_queue.append(processes[i])
            i += 1

        if not ready_queue:
            # Jump to next arrival if queue is empty.
            current_time = processes[i].arrival_time
            ready_queue.append(processes[i])
            i += 1

        current_process = ready_queue.popleft()
        run_time = min(quantum, current_process.remaining_time)
        current_process.remaining_time -= run_time
        current_time += run_time

        # Add any new arrivals during this quantum.
        while i < n and processes[i].arrival_time <= current_time:
            ready_queue.append(processes[i])
            i += 1

        if current_process.remaining_time == 0:
            current_process.completion_time = current_time
            current_process.turnaround_time = current_process.completion_time - current_process.arrival_time
            current_process.waiting_time = current_process.turnaround_time - current_process.burst_time
            total_waiting += current_process.waiting_time
            total_turnaround += current_process.turnaround_time
            completed += 1
        else:
            ready_queue.append(current_process)

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
