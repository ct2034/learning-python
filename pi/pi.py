#!/usr/bin/env python
import sys
from random import random
from math import sqrt
from rich import print
from rich.panel import Panel


def sample():
    x = random()
    y = random()
    return sqrt(x ** 2 + y ** 2) < 1


if __name__ == "__main__":
    n = 0
    guess = 0.
    while True:
        try:
            n += 1
            if sample():
                guess = guess * (n - 1.) / n + (1. / n)
                sym = "+"
            else:
                guess = guess * (n - 1.) / n
                sym = "-"
        except KeyboardInterrupt:
            print()
            print(Panel(f"[blue]π[/]: [bold green]{guess*4}", expand=False))
            sys.exit(0)
