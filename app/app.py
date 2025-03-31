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

# Append current directory to sys.path to ensure imports work correctly
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Initialize the Flask application
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    # Handle POST requests (form submission)
    if request.method == "POST":
        # Get the selected scheduling algorithm from the form
        algorithm = request.form.get("algorithm")

        # Retrieve form data for processes
        process_names = request.form.getlist("process_names[]")
        arrival_str = request.form.getlist("arrival_times[]")
        burst_str = request.form.getlist("burst_times[]")
        priority_str = request.form.getlist("priorities[]")
        quantum_str = request.form.get("quantum")  # Time Quantum for Round Robin

        # Convert arrival and burst times to integers, handle invalid input
        try:
            arrival_times = [int(time) for time in arrival_str] if arrival_str else []
            burst_times = [int(time) for time in burst_str] if burst_str else []
        except ValueError:
            return "Error: Arrival times and Burst times must be valid integers."

        # If no priorities are provided, default to 0 for non-priority algorithms
        if not priority_str:
            priority_str = ['0'] * len(process_names)

        # Convert priorities to integers, handle invalid input
        priorities = []
        for p in priority_str:
            try:
                priorities.append(int(p) if p.isdigit() else 0)
            except ValueError:
                priorities.append(0)

        # Ensure the number of processes, arrival times, and burst times match
        if len(arrival_times) != len(burst_times) or len(arrival_times) != len(process_names):
            return "Error: The number of processes, arrival times, and burst times must match."

        # Create Process objects for each process
        processes = [Process(name, arrival, burst, priority) 
                     for name, arrival, burst, priority in zip(process_names, arrival_times, burst_times, priorities)]

        # Calculate max_time (total time for the longest process)
        max_time = max([arrival + burst for arrival, burst in zip(arrival_times, burst_times)])

        # Call the appropriate scheduling algorithm based on user selection
        result_data = None
        if algorithm == "SJF":
            result_data = sjf_scheduling(processes)
        elif algorithm == "SJF Preemptive":
            result_data = sjf_preemptive_scheduling(processes)
        elif algorithm == "FCFS":
            result_data = fcfs_scheduling(processes)
        elif algorithm == "Round Robin":
            try:
                # Convert quantum to integer, default to 1 if not provided
                quantum = int(quantum_str) if quantum_str else 1
            except ValueError:
                return "Error: Time Quantum must be a valid integer."
            result_data = round_robin_scheduling(processes, quantum)
        elif algorithm == "Priority":
            result_data = priority_scheduling(processes)
        elif algorithm == "Priority Preemptive":
            result_data = priority_preemptive_scheduling(processes)
        else:
            # Default result if no valid algorithm is selected
            result_data = {'rows': [], 'avg_waiting_time': 0, 'avg_turnaround_time': 0}

        # Render the results page with the calculated data
        return render_template("results.html", 
                               results=result_data["rows"],
                               avg_waiting_time=result_data["avg_waiting_time"],
                               avg_turnaround_time=result_data["avg_turnaround_time"],
                               max_time=max_time)  # Pass max_time to the template

    # Render the index page for GET requests
    return render_template("index.html")


if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)
