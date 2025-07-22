#!/usr/bin/env python3

def clean_str(input):
    if "☠" in input:
        raise Exception("I give up :(")

    return input.replace("#", "")


if __name__ == "__main__":
    print("hi! ------")
    stdin = input()
    print(f"{stdin=}")
    out = clean_str(stdin)
    print(f"{out=}")
    print("-" * 10)
