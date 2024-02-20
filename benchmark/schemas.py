from dataclasses import dataclass


@dataclass
class BenchmarkResult:
    num_processes: int
    iterations: int
    elapsed_time: float
