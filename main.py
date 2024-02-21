import typer

import benchmark
import client
import hardware

app = typer.Typer()


@app.command()
def base(duration: int = 8, initial_processes_count: int = 1):
    benchmarks = benchmark.base.start(
        duration=duration, initial_processes=initial_processes_count
    )

    cpu = hardware.get_cpu()

    computer_id = client.add_computer(cpu)
    for benchmark_row in benchmarks:
        client.add_benchmark(
            threads=benchmark_row.num_processes,
            result=benchmark_row.elapsed_time,
            computer=computer_id,
        )


if __name__ == "__main__":
    app()
