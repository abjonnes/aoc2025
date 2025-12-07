from functools import cache

SEEN = set()


@cache
def paths(lines, r, c):
    if r >= len(lines):
        return 1

    if lines[r][c] == "^":
        SEEN.add((r, c))
        return paths(lines, r + 1, c - 1) + paths(lines, r + 1, c + 1)

    return paths(lines, r + 1, c)


def run(lines):
    return paths(tuple(lines[2::2]), 0, lines[0].index("S"))


def part1(lines):
    run(lines)
    return len(SEEN)


def part2(lines):
    return run(lines)
