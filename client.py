from dataclasses import asdict
from enum import StrEnum

import requests

import hardware


class BenchmarkType(StrEnum):
    MULTIPROCESSING = "MP"
    TORCH_TENSOR_OPERATIONS = "TTO"


class CPUClient:
    def __init__(self, cpu: hardware.CPUInfo) -> None: ...

    def get(): ...
class ComputerClient: ...


class Client: ...


def add_computer(
    cpu: hardware.CPUInfo,
    gpu: hardware.GPUInfo | None = None,
    endpoint: str = "http://127.0.0.1:8000/computers/",
    endpoint_cpus: str = "http://127.0.0.1:8000/cpus/",
):
    cpu_info = asdict(cpu)
    computers = {"cpu": cpu_info}

    if gpu:
        computers["gpu"] = asdict(gpu)

    response = requests.get(url=f"{endpoint_cpus}{cpu.name}/")
    if response.status_code == 200:
        cpu_id = response.json()["id"]
    else:
        response = requests.post(url=endpoint_cpus, json=cpu_info)
        if response.status_code == 400:
            raise ValueError(response.text)
        cpu_id = response.json()["id"]

    response = requests.post(url=endpoint, json={"cpu": cpu_id})

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


if __name__ == "__main__":
    cpu = hardware.get_cpu()

    computer_id = add_computer(cpu)
