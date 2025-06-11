import time

from rich.live import Live
from rich.table import Table

from random import random

table = Table()
table.add_column("Row ID")
table.add_column("Description")
table.add_column("Level")

with Live(table, refresh_per_second=4) as live:  # update 4 times a second to feel fluid
    for row in range(12):
        # live.console.print(f"Working on row #{row}")
        time.sleep(0.4)
        if random() > .8:
            table.add_row(f"{row}", f"description {row}", "[red]ERROR")
        else:
            table.add_row(f"{row}", f"description {row}", "[green]HÄÄ")