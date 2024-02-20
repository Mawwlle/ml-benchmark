from cpuinfo import get_cpu_info


def get_cpu_name() -> str:
    return get_cpu_info()["brand_raw"]


def get_cpu_frequency() -> float:
    return float(get_cpu_info()["hz_advertised_friendly"].split(" ")[0])
