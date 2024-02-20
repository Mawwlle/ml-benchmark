import math
import multiprocessing
import time
from typing import Callable

from benchmark.schemas import BenchmarkResult


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


def timer(
    func: Callable[[int, int], int], duration: int, num_processes: int
) -> BenchmarkResult:
    start_time = time.time()
    iterations = func(duration, num_processes)
    end_time = time.time()

    elapsed_time = end_time - start_time
    inaccuracy = duration / 10

    if elapsed_time > duration + inaccuracy:
        print(elapsed_time, iterations, num_processes)
        raise ValueError("Too long!")

    print(f"Processes: {num_processes}; Result {iterations}; Time {elapsed_time}")
    return BenchmarkResult(num_processes, iterations, elapsed_time)


def start(duration: int = 30, initial_processes: int = 1) -> list[BenchmarkResult]:
    num_processes_list = [initial_processes]
    benchmark_results: list[BenchmarkResult] = []
    multiprocessing.freeze_support()
    multiprocessing.set_start_method("spawn")

    max_iterations = 0
    while True:
        num_processes = num_processes_list[-1] * 2

        try:
            result = timer(run_test, duration, num_processes)
        except ValueError:
            break

        benchmark_results.append(result)
        num_processes_list.append(num_processes)

        if result.iterations < max_iterations:
            break
        else:
            max_iterations = result.iterations

    if len(num_processes_list) > 1:
        prev_processes = num_processes_list[-2]
        curr_processes = num_processes_list[-1]
        optimal_processes = (curr_processes + prev_processes) // 2
        try:
            result = timer(run_test, duration, optimal_processes)
        except ValueError:
            ...
        else:
            benchmark_results.append(result)

    return benchmark_results
