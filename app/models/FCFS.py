from .process import Process

#  Simulates the First-Come, First-Served (FCFS) scheduling algorithm.
#     This function calculates the waiting time, turnaround time, and completion time 
#     for a list of processes based on their arrival and burst times. It also computes 
#     the average waiting time and average turnaround time for the given processes.
#     Args:
#         processes (list): A list of Process objects. Each Process object is expected 
#                           to have the following attributes:
#                           - name (str): The name or identifier of the process.
#                           - arrival_time (int): The time at which the process arrives.
#                           - burst_time (int): The time required by the process to execute.
#                           - priority (int): The priority of the process (optional, not used in FCFS).
#     Returns:
#         dict: A dictionary containing the following keys:
#               - 'rows' (list): A list of dictionaries, each representing a process with 
#                               the following keys:
#                               - 'process' (str): The name of the process.
#                               - 'arrival' (int): The arrival time of the process.
#                               - 'burst' (int): The burst time of the process.
#                               - 'priority' (int): The priority of the process.
#                               - 'waiting' (int): The waiting time of the process.
#                               - 'turnaround' (int): The turnaround time of the process.
#                               - 'completion' (int): The completion time of the process.
#               - 'avg_waiting_time' (float): The average waiting time of all processes.
#               - 'avg_turnaround_time' (float): The average turnaround time of all processes.
#     Notes:
#         - If the list of processes is empty, the function returns default values with 
#           zero averages and an empty 'rows' list.
#         - Processes are scheduled in the order of their arrival times. If two processes 
#           have the same arrival time, they are executed in the order they appear in the list.
#         - The function assumes that all processes arrive at or after time 0.
#     Example:
#         processes = [
#             Process(name="P1", arrival_time=0, burst_time=5, priority=1),
#             Process(name="P2", arrival_time=2, burst_time=3, priority=2),
#             Process(name="P3", arrival_time=4, burst_time=1, priority=3)
#         ]
#         result = fcfs_scheduling(processes)
#         print(result)

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
            # dictinary with default values
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
