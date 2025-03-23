import sys
import os
from flask import Flask, render_template, request
from models.FCFS import fcfs_scheduling
from models.SJF_preemptive import sjf_preemptive_scheduling
from models.Round_Robin import round_robin_scheduling
from models.Priority_scheduling import priority_scheduling
from models.Priority_scheduling_preemptive import priority_preemptive_scheduling
from models.process import Process
from models.SJF import sjf_scheduling


# Append current directory to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        algorithm = request.form.get("algorithm")

        # Get the form data
        process_names = request.form.getlist("process_names[]")
        arrival_str = request.form.getlist("arrival_times[]")
        burst_str = request.form.getlist("burst_times[]")
        priority_str = request.form.getlist("priorities[]")
        quantum_str = request.form.get("quantum")  # For Round Robin, Time Quantum

        # Convert arrival and burst times to integers
        try:
            arrival_times = [int(time) for time in arrival_str] if arrival_str else []
            burst_times = [int(time) for time in burst_str] if burst_str else []
        except ValueError:
            return "Error: Arrival times and Burst times must be valid integers."

        # If no priorities are provided (for non-priority algorithms), set to 0
        if not priority_str:
            priority_str = ['0'] * len(process_names)

        # Convert priorities to integers, handle invalid input
        priorities = []
        for p in priority_str:
            try:
                priorities.append(int(p) if p.isdigit() else 0)
            except ValueError:
                priorities.append(0)

        # Check if lists have the same length
        if len(arrival_times) != len(burst_times) or len(arrival_times) != len(process_names):
            return "Error: The number of processes, arrival times, and burst times must match."

        # Create Process objects
        processes = [Process(name, arrival, burst, priority) 
                     for name, arrival, burst, priority in zip(process_names, arrival_times, burst_times, priorities)]

        # Call the correct scheduling algorithm
        result_data = None
        if algorithm == "SJF":
            result_data = sjf_scheduling(processes)
        elif algorithm == "SJF Preemptive":
            result_data = sjf_preemptive_scheduling(processes)
        elif algorithm == "FCFS":
            result_data = fcfs_scheduling(processes)
        elif algorithm == "Round Robin":
            try:
                quantum = int(quantum_str) if quantum_str else 1  # Default quantum to 1 if not provided
            except ValueError:
                return "Error: Time Quantum must be a valid integer."
            result_data = round_robin_scheduling(processes, quantum)
        elif algorithm == "Priority":
            result_data = priority_scheduling(processes)
        elif algorithm == "Priority Preemptive":
            result_data = priority_preemptive_scheduling(processes)
        else:
            result_data = {'rows': [], 'avg_waiting_time': 0, 'avg_turnaround_time': 0}

        # Render the results page
        return render_template("results.html", results=result_data["rows"],
                               avg_waiting_time=result_data["avg_waiting_time"],
                               avg_turnaround_time=result_data["avg_turnaround_time"])

    # Render the index page if the method is GET
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
