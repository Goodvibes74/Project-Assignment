# run.py
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, render_template, request
from models.FCFS import fcfs_scheduling
from models.SJF import sjf_scheduling
from models.SJF_preemptive import sjf_preemptive_scheduling
from models.Round_Robin import round_robin_scheduling
from models.Priority_scheduling import priority_scheduling
from models.Priority_scheduling_preemptive import priority_preemptive_scheduling
from models.process import Process

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        algorithm = request.form.get("algorithm")
        processes_str = request.form.get("processes")  # e.g., "P1,P2,P3"
        arrival_str = request.form.get("arrival_times")  # e.g., "0,1,2"
        burst_str = request.form.get("burst_times")      # e.g., "5,3,8"
        priority_str = request.form.get("priorities")      # e.g., "2,1,3"
        quantum_str = request.form.get("quantum")          # for Round Robin

        process_names = [x.strip() for x in processes_str.split(",")]
        arrival_times = list(map(int, arrival_str.split(",")))
        burst_times = list(map(int, burst_str.split(",")))
        # For priority algorithms, parse priorities if provided.
        priorities = list(map(int, priority_str.split(","))) if priority_str else [0] * len(process_names)

        # Create Process objects
        processes = []
        for i in range(len(process_names)):
            processes.append(Process(
                process_names[i],
                arrival_times[i],
                burst_times[i],
                priorities[i]
            ))

        result_data = None
        if algorithm == "FCFS":
            result_data = fcfs_scheduling(processes)
        elif algorithm == "SJF":
            result_data = sjf_scheduling(processes)
        elif algorithm == "SJF Preemptive":
            result_data = sjf_preemptive_scheduling(processes)
        elif algorithm == "Round Robin":
            quantum = int(quantum_str) if quantum_str else 1
            result_data = round_robin_scheduling(processes, quantum)
        elif algorithm == "Priority":
            result_data = priority_scheduling(processes)
        elif algorithm == "Priority Preemptive":
            result_data = priority_preemptive_scheduling(processes)
        else:
            result_data = {'rows': [], 'avg_waiting_time': 0, 'avg_turnaround_time': 0}

        return render_template("results.html", results=result_data["rows"],
                               avg_waiting_time=result_data["avg_waiting_time"],
                               avg_turnaround_time=result_data["avg_turnaround_time"])

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
