# app/models/process.py

class Process:
    """
    Class representing a process.
    For priority scheduling, 'priority' defaults to 0 (can be overwritten).
    """
    def __init__(self, name, arrival_time, burst_time, priority=0):
        self.name = name
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time  # used in preemptive scheduling
        self.priority = priority

        self.waiting_time = 0
        self.turnaround_time = 0
        self.completion_time = 0
