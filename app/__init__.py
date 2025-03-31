import sys
import os

# Add the current directory to the system path for module imports
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, render_template, request
from app.models.FCFS import fcfs_scheduling
from app.models.SJF import sjf_scheduling
from app.models.SJF_preemptive import sjf_preemptive_scheduling
from app.models.Round_Robin import round_robin_scheduling
from app.models.Priority_scheduling import priority_scheduling
from app.models.Priority_scheduling_preemptive import priority_preemptive_scheduling
from app.models.process import Process

# Initialize the Flask application
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Handle the main route for the application.
    - On GET: Render the index.html template.
    - On POST: Process the scheduling algorithm based on user input.
    """
    if request.method == "POST":
        # Retrieve form data
        algorithm = request.form.get("algorithm")  # Selected scheduling algorithm
        processes_str = request.form.get("processes")  # Process names (e.g., "P1,P2,P3")
        arrival_str = request.form.get("arrival_times")  # Arrival times (e.g., "0,1,2")
        burst_str = request.form.get("burst_times")  # Burst times (e.g., "5,3,8")
        priority_str = request.form.get("priorities")  # Priorities (e.g., "2,1,3")
        quantum_str = request.form.get("quantum")  # Time quantum for Round Robin

        # Parse input strings into lists
        process_names = [x.strip() for x in processes_str.split(",")]
        arrival_times = list(map(int, arrival_str.split(",")))
        burst_times = list(map(int, burst_str.split(",")))
        # Parse priorities if provided, otherwise default to 0
        priorities = list(map(int, priority_str.split(","))) if priority_str else [0] * len(process_names)

        # Create a list of Process objects
        processes = []
        for i in range(len(process_names)):
            processes.append(Process(
                process_names[i],
                arrival_times[i],
                burst_times[i],
                priorities[i]
            ))

        # Initialize result data
        result_data = None

        # Determine which scheduling algorithm to use
        if algorithm == "FCFS":
            result_data = fcfs_scheduling(processes)
        elif algorithm == "SJF":
            result_data = sjf_scheduling(processes)
        elif algorithm == "SJF Preemptive":
            result_data = sjf_preemptive_scheduling(processes)
        elif algorithm == "Round Robin":
            # Use the provided quantum or default to 1
            quantum = int(quantum_str) if quantum_str else 1
            result_data = round_robin_scheduling(processes, quantum)
        elif algorithm == "Priority":
            result_data = priority_scheduling(processes)
        elif algorithm == "Priority Preemptive":
            result_data = priority_preemptive_scheduling(processes)
        else:
            # Default result if no valid algorithm is selected
            result_data = {'rows': [], 'avg_waiting_time': 0, 'avg_turnaround_time': 0}

        # Render the results page with the computed data
        return render_template("results.html", results=result_data["rows"],
                               avg_waiting_time=result_data["avg_waiting_time"],
                               avg_turnaround_time=result_data["avg_turnaround_time"])

    # Render the index page for GET requests
    return render_template("index.html")

if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)