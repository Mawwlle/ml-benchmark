from dataclasses import asdict, dataclass
from enum import StrEnum

import requests


@dataclass
class CPUInfo:
    name: str
    frequency: float


@dataclass
class GPUInfo:
    name: str
    memory: int


class BenchmarkType(StrEnum):
    MULTIPROCESSING = "MP"
    TORCH_TENSOR_OPERATIONS = "TTO"


def add_computer(
    cpu: CPUInfo,
    gpu: GPUInfo | None = None,
    endpoint: str = "http://127.0.0.1:8000/computers/",
):
    cpu_info = asdict(cpu)
    computers = {"cpu": cpu_info}

    if gpu:
        computers["gpu"] = asdict(gpu)

    response = requests.post(url=endpoint, json=computers)

    if response.status_code == 201:
        return response.json()["id"]

    raise ValueError(response.text)


def add_benchmark(
    threads: int,
    result: float,
    computer: int,
    benchmark_type: BenchmarkType = BenchmarkType.MULTIPROCESSING,
    endpoint: str = "http://127.0.0.1:8000/benchmarks/",
):
    response = requests.post(
        url=endpoint,
        json={
            "threads": threads,
            "result": result,
            "computer": computer,
            "type": benchmark_type.value,
        },
    )

    if response.status_code == 201:
        return response.json()["id"]

    raise ValueError(response.text)
