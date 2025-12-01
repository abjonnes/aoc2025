import os
from importlib import import_module
from inspect import signature
from pathlib import Path

import click
import requests

INPUT_URL = "https://adventofcode.com/2025/day/{day}/input"
TOKEN_ENVVAR = "AOC_SESSION"
TOKEN_FILE = Path(".aoc_session")


def get_token():
    token = os.environ.get(TOKEN_ENVVAR)
    
    if not token and TOKEN_FILE.exists():
        token = TOKEN_FILE.read_text().strip()

    if not token:
        raise RuntimeError(
            f"AOC session token required in `{TOKEN_FILE}` file or `{TOKEN_ENVVAR}` environment variable"
        )

    return token


def get_input(day):
    response = requests.get(INPUT_URL.format(day=day), cookies={"session": get_token()})
    response.raise_for_status()
    return response.text


def format_output(output):
    if isinstance(output, str) and "\n" in output:
        return "\n" + output
    return str(output)


def run_part(part, data):
    sig = signature(part)
    args = dict()
    if "data" in sig.parameters:
        args["data"] = data
    if "lines" in sig.parameters:
        lines = data.split("\n")

        # remove the line resulting from the last newline
        if not lines[-1]:
            lines.pop()

        args["lines"] = lines

    return part(**args)


def set_up_profiling():
    import atexit
    import cProfile
    import io
    import pstats

    pr = cProfile.Profile()
    pr.enable()

    def exit():
        pr.disable()
        s = io.StringIO()
        pstats.Stats(pr, stream=s).sort_stats("cumulative").print_stats()
        print(s.getvalue())

    atexit.register(exit)


@click.command()
@click.option("--profile", is_flag=True)
@click.argument("day", type=int, required=True)
def aoc(profile, day):
    module = import_module(f"aoc.day{day}")

    data = get_input(day)

    if profile:
        set_up_profiling()

    try:
        print(f"Part 1: {format_output(run_part(module.part1, data))}")

        if hasattr(module, "part2"):
            print(f"Part 2: {format_output(run_part(module.part2, data))}")
    except KeyboardInterrupt:
        import sys
        import traceback

        traceback.print_exc(file=sys.stdout)
