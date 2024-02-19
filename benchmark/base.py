import math
import time
import multiprocessing
from typing import Callable

def compute_task(iterations: int) -> int:
    result = 0
    
    for _ in range(iterations):
        math.sin(math.radians(45))
        result += 1
        
    return result

def run_test(duration_seconds: int, num_processes: int) -> int:
    start_time = time.time()
    iterations = 0
    
    while time.time() - start_time < duration_seconds:
        with multiprocessing.Pool(num_processes) as p:
            p.map(compute_task, [10000] * num_processes)
        
        iterations += num_processes
    
    return iterations

def timer(func: Callable[[int, int], int], duration: int, num_processes: int) -> int:
    start_time = time.time()
    iterations = func(duration, num_processes)
    end_time = time.time()
   
    elapsed_time = end_time - start_time
   
    print(f"{num_processes} Processes - Iterations: {iterations}, Time: {elapsed_time:.2f} seconds") # TODO: fix
    
    return iterations

def start(duration: int = 30, initial_processes: int = 1) -> None:
    num_processes_list = [initial_processes]
    
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
        
    print("Benchmarking...")
    max_iterations = 0
    while True:
        num_processes = num_processes_list[-1] * 2 
        iterations = timer(run_test, duration, num_processes)
        num_processes_list.append(num_processes)
        
        if iterations < max_iterations:
            break 
        else:
            max_iterations = iterations
    
    if len(num_processes_list) > 1:
        prev_processes = num_processes_list[-2]
        curr_processes = num_processes_list[-1]
        optimal_processes = (curr_processes + prev_processes) // 2
        timer(run_test, duration, optimal_processes)
