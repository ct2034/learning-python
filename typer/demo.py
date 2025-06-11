import sys

import numpy as np
from typing_extensions import Annotated

import typer
from rich import print
from rich.panel import Panel

app = typer.Typer()


@app.command()
def calculate(
    samples: Annotated[
        int, typer.Argument(help="How many samples to use to calculate pi.")
    ],
    useless: float = 0.99,
):
    """Calculate π using random samples."""
    if samples > 100000000:
        print(
            Panel(
                "[red]Too [bold]many[/bold] samples.",
                title="[bold]Problem",
                subtitle="Sorry ...",
                expand=False,
            )
        )
        sys.exit(1)
    d = np.random.random((2, samples))
    r = np.sqrt(np.pow(d[0, :], 2) + np.pow(d[1, :], 2))
    π = 4 * np.count_nonzero(r < 1) / samples
    print(
        Panel(
            f"[blue]π[/]: [bold green]{π}[/] ({useless} ?!)",
            title="[bold]Result",
            subtitle="hihi ...",
            expand=False,
        )
    )


if __name__ == "__main__":
    app()
