# CPUTaskSched 

**CPUTaskSched** is a Python-based CPU scheduling simulator that visualizes and compares the execution of various scheduling algorithms. It includes support for algorithms like **FCFS**, **SPN**, **HRRN**, **RR**, and **SRTF**. You can input your own processes, adjust parameters like context switch time and time quantum, and get both visual Gantt charts and tabular metrics (e.g., waiting time, turnaround time, response time).

---

## Features ✨

- Simulates multiple CPU scheduling algorithms:
  - **First-Come, First-Served (FCFS)**
  - **Shortest Process Next (SPN)**
  - **Highest Response Ratio Next (HRRN)**
  - **Round Robin (RR)**
  - **Shortest Remaining Time First (SRTF)**

- Provides Gantt chart visualizations for each algorithm
- Displays detailed process metrics: wait time, turnaround time, and response time
- Customizable time quantum and context switch time

---

## Installation 💻

1. **Clone the repository:**

   ```bash
   git clone https://github.com/CS-Astronaut/CPUTaskSched.git
   ```

2. **Navigate into the project directory:**

   ```bash
   cd CPUTaskSched
   ```

3. **Install required dependencies:**

   Make sure you have **Python 3.x** installed, then install the required packages using `pip`:

   ```bash
   pip install numpy tkinter matplotlib
   ```

   This will install all the necessary libraries, including:
   - `tkinter` (for the GUI)
   - `matplotlib` (for Gantt chart visualizations)
   - `numpy` (needed for processing)

---

## Usage 🛠️

1. **Run the application:**

   To start the CPU scheduling simulator, run the following command:

   ```bash
   python CPUTaskSched.py
   ```

   This will open a graphical user interface (GUI) where you can input process data and customize settings like context switch time and time quantum.

2. **Input format:**

   In the GUI, you will be prompted to input a list of processes in the format:

   ```plaintext
   [[CBT1, AT1], [CBT2, AT2], ...]
   ```

   Where:
   - **CBT** = CPU Burst Time
   - **AT** = Arrival Time

   Example input:

   ```plaintext
   [[5, 0], [8, 1], [3, 2]]
   ```

3. **Choose scheduling algorithm:**

   After inputting the process data, select an algorithm from the dropdown list. The available options are:
   - FCFS
   - SPN
   - HRRN
   - RR
   - SRTF

4. **View Results:**

   - After running the simulation, the program will display:
     - Gantt charts visualizing the execution of each algorithm
     - A table with process metrics (Wait Time, Turnaround Time, Response Time)
     - A summary of the average metrics for each algorithm

---

## Example 💡

Here’s an example of input and output:

### Input:
```plaintext
[[5, 0], [8, 1], [3, 2]]
```

### Output:
- **Gantt Chart** showing process execution for each algorithm.
- **Metrics Table** showing the wait time, turnaround time, and response time for each process.
- **Average Metrics Summary** comparing the different algorithms.

---
