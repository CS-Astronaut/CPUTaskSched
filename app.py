import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CPUScheduler:
    def __init__(self):
        self.processes = []  # Input: [[CBT1, AT1], [CBT2, AT2], ...]
        self.context_switch_time = 0
        self.time_quantum = 5

    def fcfs(self):
        n = len(self.processes)
        CBT = [p[0] for p in self.processes]
        AT = [p[1] for p in self.processes]
        WT = [0] * n
        TT = [0] * n
        RT = [0] * n
        gantt = []

        # Sort processes by arrival time
        sorted_processes = sorted(enumerate(self.processes), key=lambda x: x[1][1])
        time = sorted_processes[0][1][1]  # Start with first arrival

        first_process = True  # Flag to indicate the first process

        for i, (cbt, at) in sorted_processes:
            if time < at:
                time = at

            gantt.append((at, at, i, "arrival"))  # Add process arrival

            # Add context switch only if not the first process
            if not first_process and self.context_switch_time > 0:
                gantt.append((time, time + self.context_switch_time, -1, "context_switch"))
                time += self.context_switch_time

            gantt.append((time, time + cbt, i, "execution"))
            WT[i] = time - at
            RT[i] = WT[i]
            TT[i] = WT[i] + cbt
            time += cbt

            first_process = False  # First process is now executed

        return gantt, WT, TT, RT

    def spn(self):
        n = len(self.processes)
        CBT = [p[0] for p in self.processes]
        AT = [p[1] for p in self.processes]
        WT = [0] * n
        TT = [0] * n
        RT = [0] * n
        gantt = []

        completed = [False] * n
        time = min(AT)
        first_process = True  # Flag to indicate the first process

        while True:
            if all(completed):
                break

            available = [(i, CBT[i]) for i in range(n) if not completed[i] and AT[i] <= time]

            if not available:
                time = min(AT[i] for i in range(n) if not completed[i])
                continue

            # Choose process with shortest burst time
            current = min(available, key=lambda x: x[1])[0]

            gantt.append((AT[current], AT[current], current, "arrival"))  # Add process arrival

            # Add context switch only if not the first process
            if not first_process and self.context_switch_time > 0:
                gantt.append((time, time + self.context_switch_time, -1, "context_switch"))
                time += self.context_switch_time

            gantt.append((time, time + CBT[current], current, "execution"))
            WT[current] = time - AT[current]
            RT[current] = WT[current]
            TT[current] = WT[current] + CBT[current]
            time += CBT[current]
            completed[current] = True

            first_process = False  # First process is now executed

        return gantt, WT, TT, RT

    def hrrn(self):
        n = len(self.processes)
        CBT = [p[0] for p in self.processes]
        AT = [p[1] for p in self.processes]
        WT = [0] * n
        TT = [0] * n
        RT = [0] * n
        gantt = []

        completed = [False] * n
        time = min(AT)
        first_process = True  # Flag to indicate the first process

        while True:
            if all(completed):
                break

            # Calculate response ratio for available processes
            available = []
            for i in range(n):
                if not completed[i] and AT[i] <= time:
                    wait_time = time - AT[i]
                    response_ratio = (wait_time + CBT[i]) / CBT[i]
                    available.append((i, response_ratio))

            if not available:
                time = min(AT[i] for i in range(n) if not completed[i])
                continue

            # Choose process with highest response ratio
            current = max(available, key=lambda x: x[1])[0]

            gantt.append((AT[current], AT[current], current, "arrival"))  # Add process arrival

            # Add context switch only if not the first process
            if not first_process and self.context_switch_time > 0:
                gantt.append((time, time + self.context_switch_time, -1, "context_switch"))
                time += self.context_switch_time

            gantt.append((time, time + CBT[current], current, "execution"))
            WT[current] = time - AT[current]
            RT[current] = WT[current]
            TT[current] = WT[current] + CBT[current]
            time += CBT[current]
            completed[current] = True

            first_process = False  # First process is now executed

        return gantt, WT, TT, RT

    def rr(self):
        n = len(self.processes)
        CBT = [p[0] for p in self.processes]
        AT = [p[1] for p in self.processes]
        WT = [0] * n
        TT = [0] * n
        RT = [-1] * n  # Initialize RT to -1
        gantt = []

        remaining = CBT.copy()
        time = min(AT)
        ready_queue = []
        first_process = True  # Flag to indicate the first process

        while True:
            # Add newly arrived processes to ready queue
            for i in range(n):
                if AT[i] <= time and remaining[i] > 0 and i not in ready_queue:
                    ready_queue.append(i)

            if not ready_queue:
                if all(remaining[i] == 0 for i in range(n)):
                    break
                time = min(AT[i] for i in range(n) if remaining[i] > 0)
                continue

            current = ready_queue.pop(0)

            # Add process arrival as a circle
            if remaining[current] == CBT[current]:
                gantt.append((AT[current], AT[current], current, "arrival"))

            # Add context switch only if not the first process
            if not first_process and self.context_switch_time > 0:
                gantt.append((time, time + self.context_switch_time, -1, "context_switch"))
                time += self.context_switch_time

            # Record first response time
            if RT[current] == -1:
                RT[current] = time - AT[current]

            # Execute for quantum or remaining time
            execute_time = min(self.time_quantum, remaining[current])
            gantt.append((time, time + execute_time, current, "execution"))

            remaining[current] -= execute_time
            time += execute_time

            # If process not finished, add back to queue
            if remaining[current] > 0:
                ready_queue.append(current)
            else:
                TT[current] = time - AT[current]
                WT[current] = TT[current] - CBT[current]

            first_process = False  # First process is now executed

        return gantt, WT, TT, RT

    def srtf(self):
        n = len(self.processes)
        CBT = [p[0] for p in self.processes]
        AT = [p[1] for p in self.processes]
        remaining = CBT.copy()
        WT = [0] * n
        TT = [0] * n
        RT = [-1] * n
        gantt = []

        time = min(AT)
        completed = 0
        current_process = None
        last_process = None
        first_process = True  # Flag to indicate the first process

        while completed < n:
            # Find process with minimum remaining time
            min_remaining = float('inf')
            current_process = None

            for i in range(n):
                if AT[i] <= time and remaining[i] > 0:
                    if remaining[i] < min_remaining:
                        min_remaining = remaining[i]
                        current_process = i

            if current_process is None:
                time = min(AT[i] for i in range(n) if remaining[i] > 0)
                continue

            # Add process arrival as a circle
            if remaining[current_process] == CBT[current_process]:
                gantt.append((AT[current_process], AT[current_process], current_process, "arrival"))

            # Add context switch only if switching processes and not the first process
            if last_process is not None and last_process != current_process and not first_process and self.context_switch_time > 0:
                gantt.append((time, time + self.context_switch_time, -1, "context_switch"))
                time += self.context_switch_time

            # Record first response time
            if RT[current_process] == -1:
                RT[current_process] = time - AT[current_process]

            gantt.append((time, time + 1, current_process, "execution"))
            remaining[current_process] -= 1

            if remaining[current_process] == 0:
                completed += 1
                TT[current_process] = time + 1 - AT[current_process]
                WT[current_process] = TT[current_process] - CBT[current_process]

            last_process = current_process
            time += 1
            first_process = False  # First process is now executed

        return gantt, WT, TT, RT



class SchedulerApp:
    def __init__(self, root):
        self.scheduler = CPUScheduler()
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.create_widgets()

    def create_widgets(self):
        # Configure the root grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        self.root.grid_rowconfigure(0, weight=1)

        # Input section
        input_frame = tk.Frame(self.root)
        input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        input_frame.grid_rowconfigure(6, weight=1)  # Allow the "Run" button space to expand

        tk.Label(input_frame, text="Processes (CBT, AT) as List:").grid(row=0, column=0, sticky="w")
        self.process_input = tk.Text(input_frame, width=30, height=5)
        self.process_input.grid(row=1, column=0, pady=5)

        tk.Label(input_frame, text="Context Switch Time:").grid(row=2, column=0, sticky="w")
        self.cs_input = tk.Entry(input_frame)
        self.cs_input.grid(row=3, column=0, pady=5)
        self.cs_input.insert(0, "0")

        tk.Label(input_frame, text="Time Quantum:").grid(row=4, column=0, sticky="w")
        self.tq_input = tk.Entry(input_frame)
        self.tq_input.grid(row=5, column=0, pady=5)
        self.tq_input.insert(0, "5")

        self.run_button = tk.Button(input_frame, text="Run", command=self.run_simulation)
        self.run_button.grid(row=6, column=0, pady=10, sticky="s")

        # Scrollable output section
        scrollable_frame = tk.Frame(self.root)
        scrollable_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        canvas = tk.Canvas(scrollable_frame)
        canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = tk.Scrollbar(scrollable_frame, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        canvas.configure(yscrollcommand=scrollbar.set)
        self.output_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.output_frame, anchor="nw")
        self.output_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        scrollable_frame.grid_rowconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(0, weight=1)

    def run_simulation(self):
        try:
            self.scheduler.processes = eval(self.process_input.get("1.0", "end").strip())
            if not all(isinstance(p, list) and len(p) == 2 for p in self.scheduler.processes):
                raise ValueError("Input must be a list of [CBT, AT] pairs.")
        except Exception as e:
            messagebox.showerror("Input Error", f"Invalid input format. Error: {e}")
            return

        self.scheduler.context_switch_time = int(self.cs_input.get())
        self.scheduler.time_quantum = int(self.tq_input.get())

        for widget in self.output_frame.winfo_children():
            widget.destroy()

        algorithms = ["FCFS", "SPN", "HRRN", "RR", "SRTF"]
        averages = []

        for i, algo in enumerate(algorithms):
            gantt, WT, TT, RT = getattr(self.scheduler, algo.lower())()

            avg_wt = sum(WT) / len(WT)
            avg_tt = sum(TT) / len(TT)
            avg_rt = sum(RT) / len(RT)
            averages.append((algo, avg_wt, avg_tt, avg_rt))

            fig, ax = plt.subplots(figsize=(8, 2))

            for (start, end, process, event) in gantt:
                if event == "arrival":
                    ax.plot(start, process, "o", color="green", label="Arrival" if i == 0 else "")
                elif event == "execution":
                    ax.plot([start, end], [process, process], color="blue", lw=2, label="Execution" if i == 0 else "")
                elif event == "context_switch":
                    ax.plot([start, end], [process, process], color="red", linestyle="dotted", label="Context Switch" if i == 0 else "")

            ax.set_yticks(range(len(self.scheduler.processes)))
            ax.set_yticklabels([f"P{i+1}" for i in range(len(self.scheduler.processes))])
            ax.set_xlabel("Time", fontsize=10) 
            ax.set_title(algo, fontsize=12)
            ax.grid(True, linestyle="--", alpha=0.5)
            plt.tight_layout()
            # ax.legend()

            canvas = FigureCanvasTkAgg(fig, self.output_frame)
            canvas.get_tk_widget().grid(row=i, column=0, padx=10, pady=10, sticky="nsew")

            table_frame = tk.Frame(self.output_frame)
            table_frame.grid(row=i, column=1, padx=10, pady=10, sticky="nsew")
            ttk.Label(table_frame, text=f"{algo} WT, TT, RT").grid(row=0, column=0)
            for j, (wt, tt, rt) in enumerate(zip(WT, TT, RT)):
                ttk.Label(table_frame, text=f"P{j+1}: WT={wt}, TT={tt}, RT={rt}").grid(row=j + 1, column=0)
    


        # Add summary table
        summary_frame = tk.Frame(self.output_frame)
        summary_frame.grid(row=len(algorithms), column=0, columnspan=2, pady=10)

        tk.Label(summary_frame, text="Average WT, TT, RT", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=4)
        tk.Label(summary_frame, text="Algorithm").grid(row=1, column=0, padx=5)
        tk.Label(summary_frame, text="Avg WT").grid(row=1, column=1, padx=5)
        tk.Label(summary_frame, text="Avg TT").grid(row=1, column=2, padx=5)
        tk.Label(summary_frame, text="Avg RT").grid(row=1, column=3, padx=5)

        for i, (algo, avg_wt, avg_tt, avg_rt) in enumerate(averages):
            tk.Label(summary_frame, text=algo).grid(row=i+2, column=0)
            tk.Label(summary_frame, text=f"{avg_wt:.2f}").grid(row=i+2, column=1)
            tk.Label(summary_frame, text=f"{avg_tt:.2f}").grid(row=i+2, column=2)
            tk.Label(summary_frame, text=f"{avg_rt:.2f}").grid(row=i+2, column=3)


if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()