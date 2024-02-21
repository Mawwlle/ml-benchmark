from dataclasses import dataclass

from cpuinfo import get_cpu_info


@dataclass
class CPUInfo:
    name: str
    frequency: float
    arch: str
    bits: int
    count: int
    l1_data_cache_size: int | None
    l1_instruction_cache_size: int | None
    l2_cache_size: int
    l2_cache_line_size: int
    l2_cache_associativity: int
    l3_cache_size: int | None
    stepping: int
    model: int


def get_cpu() -> CPUInfo:
    cpu_info = get_cpu_info()

    return CPUInfo(
        name=cpu_info["brand_raw"],
        frequency=cpu_info["hz_advertised"][0],
        arch=cpu_info["arch"],
        bits=cpu_info["bits"],
        count=cpu_info["count"],
        l1_instruction_cache_size=cpu_info.get("l1_instruction_cache_size", None),
        l1_data_cache_size=cpu_info.get("l1_data_cache_size", None),
        l2_cache_size=cpu_info["l2_cache_size"],
        l2_cache_line_size=cpu_info["l2_cache_line_size"],
        l2_cache_associativity=cpu_info["l2_cache_associativity"],
        l3_cache_size=cpu_info.get("l3_cache_size", None),
        stepping=cpu_info["stepping"],
        model=cpu_info["model"],
    )


@dataclass
class GPUInfo:
    name: str
    memory: int
