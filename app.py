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
        return self.simulate("FCFS")

    def spn(self):
        return self.simulate("SPN")

    def hrrn(self):
        return self.simulate("HRRN")

    def rr(self):
        return self.simulate("RR")

    def srtf(self):
        return self.simulate("SRTF")

    def simulate(self, algorithm):
        n = len(self.processes)
        CBT = [p[0] for p in self.processes]
        AT = [p[1] for p in self.processes]
        WT = [0] * n
        TT = [0] * n
        RT = [0] * n
        gantt = []

        if algorithm == "FCFS":
            time = 0
            for i, (cbt, at) in enumerate(sorted(self.processes, key=lambda x: x[1])):
                start = max(time, at)
                gantt.append((start, start + cbt, i))
                WT[i] = start - at
                TT[i] = WT[i] + cbt
                RT[i] = WT[i]
                time = start + cbt + self.context_switch_time

        elif algorithm == "SPN":
            time = 0
            completed = [False] * n
            for _ in range(n):
                candidates = [(i, CBT[i]) for i in range(n) if not completed[i] and AT[i] <= time]
                if not candidates:
                    time += 1
                    continue
                i, _ = min(candidates, key=lambda x: x[1])
                start = time
                gantt.append((start, start + CBT[i], i))
                WT[i] = start - AT[i]
                TT[i] = WT[i] + CBT[i]
                RT[i] = WT[i]
                time += CBT[i] + self.context_switch_time
                completed[i] = True

        elif algorithm == "HRRN":
            time = 0
            completed = [False] * n
            for _ in range(n):
                candidates = [(i, (WT[i] + CBT[i]) / CBT[i]) for i in range(n) if not completed[i] and AT[i] <= time]
                if not candidates:
                    time += 1
                    continue
                i, _ = max(candidates, key=lambda x: x[1])
                start = time
                gantt.append((start, start + CBT[i], i))
                WT[i] = start - AT[i]
                TT[i] = WT[i] + CBT[i]
                RT[i] = WT[i]
                time += CBT[i] + self.context_switch_time
                completed[i] = True

        elif algorithm == "RR":
            time = 0
            queue = [i for i in range(n)]
            remaining = CBT[:]
            while queue:
                i = queue.pop(0)
                if AT[i] > time:
                    time += 1
                    queue.append(i)
                    continue
                start = time
                run_time = min(self.time_quantum, remaining[i])
                gantt.append((start, start + run_time, i))
                remaining[i] -= run_time
                if remaining[i] > 0:
                    queue.append(i)
                else:
                    WT[i] = time - AT[i] - (CBT[i] - remaining[i])
                    TT[i] = WT[i] + CBT[i]
                    RT[i] = WT[i]
                time += run_time + self.context_switch_time

        elif algorithm == "SRTF":
            time = 0
            remaining = CBT[:]
            completed = 0
            while completed < n:
                candidates = [(i, remaining[i]) for i in range(n) if remaining[i] > 0 and AT[i] <= time]
                if not candidates:
                    time += 1
                    continue
                i, _ = min(candidates, key=lambda x: x[1])
                start = time
                gantt.append((start, start + 1, i))
                remaining[i] -= 1
                if remaining[i] == 0:
                    completed += 1
                    WT[i] = time + 1 - AT[i] - CBT[i]
                    TT[i] = WT[i] + CBT[i]
                    RT[i] = WT[i]
                time += 1

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
            for (start, end, process) in gantt:
                ax.plot([start, end], [process, process], color="blue", lw=2)

            ax.set_yticks(range(len(self.scheduler.processes)))
            ax.set_yticklabels([f"P{i+1}" for i in range(len(self.scheduler.processes))])
            ax.set_xlabel("Time", fontsize=10)
            ax.set_title(algo, fontsize=12)
            ax.grid(True, linestyle="--", alpha=0.5)
            plt.tight_layout()

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
