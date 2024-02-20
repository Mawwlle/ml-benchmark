import typer

import benchmark
import hardware
from client import CPUInfo, add_benchmark, add_computer

app = typer.Typer()


@app.command()
def base(duration: int = 8, initial_processes_count: int = 1):
    benchmarks = benchmark.base.start(
        duration=duration, initial_processes=initial_processes_count
    )

    cpu_name = hardware.get_cpu_name()
    frequency = hardware.get_cpu_frequency()

    computer_id = add_computer(CPUInfo(name=cpu_name, frequency=frequency))
    for benchmark_row in benchmarks:
        add_benchmark(
            threads=benchmark_row.num_processes,
            result=benchmark_row.elapsed_time,
            computer=computer_id,
        )


if __name__ == "__main__":
    app()
