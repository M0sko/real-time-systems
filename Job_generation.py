tasks_definition = [
    {"id": 1, "C": 2.9542, "T": 10},
    {"id": 2, "C": 3, "T": 10}, 
    {"id": 3, "C": 2, "T": 20}, 
    {"id": 4, "C": 2, "T": 20}, 
    {"id": 5, "C": 2, "T": 40}, 
    {"id": 6, "C": 2, "T": 40}, 
    {"id": 7, "C": 3, "T": 80}, 
]

hyperperiod = 80 
jobs = []

for t in tasks_definition:
    for i in range(hyperperiod // t["T"]): 
        jobs.append({
            "id": f"T{t['id']}_J{i+1}", # Unique job identifier combining task ID and job instance number (e.g., T1_J1 for the first job of task 1).
            "task_id": t["id"],   # Task ID for reference,.
            "r": i * t["T"],      # Release time (Causality)
            "C": t["C"],          # Execution time 
            "d": (i + 1) * t["T"] # Deadline
        })


jobs.sort(key=lambda x: x["r"]) # Sorts jobs by release time (causality) to ensure they are processed in the correct order. 
print(f"Number of generated jobs : {len(jobs)}")

def run_v1_scheduler(job_list):
    """
    Non-preemptive scheduler 
    Goal: No deadlines missed  + Minimize waiting 
    Strategy: Earliest Deadline First (EDF) among ready jobs
    """
    current_time = 0
    schedule = []
    remaining = list(job_list) 
    
    wait_v1 = 0
    idle_v1 = 0

    print(f"{'Job':<8} | {'Arrival':<8} | {'Start':<8} | {'End':<8} | {'Time Rep':<8} | {'Max':<5} | {'Schedulable ?'}")    
    print("-" * 70)

    while remaining:
        # Identify ready jobs (those that have arrived by current_time)
        ready_jobs = [j for j in remaining if j['r'] <= current_time]
        
        if not ready_jobs:
            # No jobs are ready, so we must idle until the next job arrives, we can skip time forward to the next arrival and add that idle time to idle_v1.
            next_arrival = min(j['r'] for j in remaining)
            idle_v1 += (next_arrival - current_time)
            current_time = next_arrival
            continue

        # Among ready jobs, select the one with the earliest deadline and execute it first non-preemptively.
        ready_jobs.sort(key=lambda x: x['d']) # Sort ready jobs by deadline
        job = ready_jobs[0]

        # Execute the selected job non-preemptively. 
        start_time = current_time
        end_time = start_time + job['C'] 
        waiting_time = start_time - job['r'] # Calculate waiting time for this job (time from release to start)
        
        rij = end_time - job['r'] # Calculate response time (time from release to completion)
        max_allowed = job['d'] - job['r'] # Calculate maximum allowed time (deadline - release time)
        schedulable = "YES" if rij <= max_allowed else "NO" # Check if the job meets its deadline based on response time and maximum allowed time
        
        # Check if the job meets its deadline and log the status accordingly.
        status = "OK" # Assume the job meets its deadline unless we find otherwise.
        if end_time > job['d']: # If the job finishes after its deadline, we consider it a deadline miss.
            status = "MISSED" 

        # Log results
        print(f"{job['id']:<8} | {job['r']:<8.1f} | {start_time:<8.5f} | {end_time:<8.5f} | {rij:<8.2f} | {max_allowed:<5.1f} | {schedulable}")    
            
        schedule.append(job)
        wait_v1 += waiting_time
        current_time = end_time
        remaining.remove(job)

    return wait_v1, idle_v1

def run_v2_scheduler(job_list):
    """
    Non-preemptive scheduler
    Goal: Allow T5 to miss deadlines to minimize waiting for other tasks
    Strategy: If T5 is ready but there are other ready jobs, ignore T5. 
    """
    current_time = 0
    schedule = []
    remaining = list(job_list) 
    
    wait_v1 = 0
    idle_v1 = 0

    print(f"{'Job':<8} | {'Arrival':<8} | {'Start':<8} | {'End':<8} | {'Time Rep':<8} | {'Max':<5} | {'Schedulable ?'}")    
    print("-" * 70)

    while remaining:
        # Identify ready jobs (those that have arrived by current_time)
        ready_jobs = [j for j in remaining if j['r'] <= current_time]
        
        if not ready_jobs:
            # No jobs are ready, so we must idle until the next job arrives, we can skip time forward to the next arrival and add that idle time to idle_v1.
            next_arrival = min(j['r'] for j in remaining)
            idle_v1 += (next_arrival - current_time)
            current_time = next_arrival
            continue

        # If T5 is ready but there are other ready jobs, we ignore T5 and pick the one with the earliest deadline among the others.
        others_ready = [j for j in ready_jobs if j['task_id'] != 5] # Keep only the ready jobs that are not T5
        
        if others_ready:
            # Amongs the other ready jobs, we pick the one with the earliest deadline
            others_ready.sort(key=lambda x: x['d']) # Sort by deadline to ensure we pick the one with the earliest deadline
            job = others_ready[0]
        else:
            # If only T5 is ready, we execute it even if it will miss its deadline, because we want to minimize waiting for other tasks.
            ready_jobs.sort(key=lambda x: x['d']) # Sort by deadline to ensure we pick T5 if it's the only ready job
            job = ready_jobs[0]

        # Execute the selected job non-preemptively.
        start_time = current_time
        end_time = start_time + job['C']
        waiting_time = start_time - job['r'] # Calculate waiting time for this job (time from release to start)
        
        rij = end_time - job['r'] # Calculate response time (time from release to completion)
        max_allowed = job['d'] - job['r'] # Calculate maximum allowed time (deadline - release time)
        schedulable = "YES" if rij <= max_allowed else "NO" # Check if the job meets its deadline based on response time and maximum allowed time
        
        # Check if the job meets its deadline and log the status accordingly.
        status = "OK" # Assume the job meets its deadline unless we find otherwise.
        if end_time > job['d']: # If the job finishes after its deadline, we consider it a deadline miss.
            status = "MISSED"

        # Log results
        print(f"{job['id']:<8} | {job['r']:<8.1f} | {start_time:<8.5f} | {end_time:<8.5f} | {rij:<8.2f} | {max_allowed:<5.1f} | {schedulable}")
        
        schedule.append(job)
        wait_v1 += waiting_time
        current_time = end_time
        remaining.remove(job)

    return wait_v1, idle_v1

# --- Comparaison --- # 

# Run both scheduler and print results
print("--- VERSION 1: NO DEADLINE MISSES ---")
wait_v1, idle_v1 = run_v1_scheduler(jobs)
print(f"Total Waiting Time (V1): {wait_v1:.2f} ms") 
print(f"Total Idle Time (V1): {idle_v1:.2f} ms \n")    


print("--- SCENARIO 2 : MINIMAL WAITING (T5 ALLOWED TO MISS) ---")
wait_v2, idle_v2 = run_v2_scheduler(jobs)
print(f"\nTotal Waiting Time (V2): {wait_v2:.4f} ms")
print(f"Total Idle Time (V2): {idle_v2:.4f} ms")

print("\n--- FINAL COMPARISON ---")
print(f"Scenario 1 Waiting: {wait_v1:.4f} | Idle: {idle_v1:.4f}")
print(f"Scenario 2 Waiting: {wait_v2:.4f} | Idle: {idle_v2:.4f}")

