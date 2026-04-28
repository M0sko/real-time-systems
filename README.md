# Real-Time Task System Analysis (In422)

This repository contains the final assignment for the **In422: Real-Time Information Systems** course. 
The project focuses on measuring Worst-Case Execution Time (WCET), performing schedulability analysis, and implementing non-preemptive scheduling algorithms for a specific real-time task set.

## 🎯 Project Goals

The objective is to analyze a system of seven tasks and ensure they can be scheduled within an 80 ms hyperperiod. The core components include:
* **WCET Estimation**: Experimentally obtaining the execution time distribution (Min, Max, Q1, Q2, Q3) for task $\tau_{1}$ to determine its WCET ($C_{1}$).
* **Schedulability Verification**: Calculating the processor utilization ($U$) to ensure the workload is handled within the given time frames.
* **Algorithm Optimization**: Developing a non-preemptive scheduler aimed at eliminating deadline misses while minimizing total waiting time.
* **Alternative Scenario Analysis**: Exploring a secondary strategy that prioritizes total waiting time minimization, even if it necessitates a deadline miss for task $\tau_{5}$.

## 📁 Repository Structure

* `multiplication.c`: Core C implementation for Task $\tau_{1}$ logic.
* `multiplication.so`: Compiled shared library used by the Python scripts.
* `wcet_mesure.py`: Benchmarking script that generates the execution time distribution.
* `Job_generation.py`: Main scheduling script that generates jobs and simulates Scenarios 1 and 2.
* `Final_Report_Eliott_Moskowicz.pdf`: The complete technical report summarizing the findings.

## 🚀 Execution Instructions

To ensure the system functions correctly, the C code must be compiled into a shared library so that Python can interface with it via `ctypes`.

### 1. Compile the C Library
Before running the measurement scripts, you must compile `multiplication.c`. Open your terminal and run:

```bash
gcc -fPIC -shared -o multiplication.so multiplication.c
```
Note: The -fPIC and -shared flags are required to create the library that Python expects.

Alternatively, you can also simply run the file in VSC if you have the proper extension and wish to avoid terminal commands. 

Once the library is compiled, execute the benchmarking script to generate the execution time statistics for $\tau_{1}$:

```bash
python3 wcet_mesure.py
```

This script collects 50,000 timing samples to capture the true Worst-Case scenario while filtering out OS-level slowdowns.
Note that you will obtain different results each time. 

Finally, run the job generation script to see the scheduling results for both Scenario 1 (Strict EDF) and Scenario 2 (Delayed $\tau_{5}$):

```bash
python3 Job_generation.py
```
## 📊 Summary of Results
The system achieves a Total Processor Utilization of 93.29% with a measured $C_{1}$ of 2.9542 ms (including a 20% safety margin).
Conclusion: The standard EDF logic proved to be the most efficient for this configuration. Delaying $\tau_{5}$ actually increased the total waiting time by 4 ms due to non-preemptive blocking factors.

Student: Eliott MOSKOWICZ   
Course: In422 - Real-Time Information Systems   
School: IPSA Toulouse
