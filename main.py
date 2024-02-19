import typer
import benchmark

app = typer.Typer()


@app.command()
def base(duration: int = 30, initial_processes_count: int = 1):
    benchmark.base.start(duration=duration, initial_processes=initial_processes_count)
    
if __name__ == "__main__":
    app()