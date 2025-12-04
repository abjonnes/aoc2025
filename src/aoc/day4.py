from itertools import product


def neighboring_rolls(lines, r, c, ignore=set()):
    cnt = 0
    n_rows = len(lines)
    n_cols = len(lines[0])
    for r2, c2 in product((r - 1, r, r + 1), (c - 1, c, c + 1)):
        if not (0 <= r2 < n_rows) or not (0 <= c2 < n_cols) or (r2, c2) == (r, c):
            continue
        if lines[r2][c2] == "@" and (r2, c2) not in ignore:
            cnt += 1
    return cnt


def part1(lines):
    return sum(
        neighboring_rolls(lines, r, c) < 4
        for r, line in enumerate(lines)
        for c, char in enumerate(line)
        if char == "@"
    )


def part2(lines):
    ignore = set()
    cnt = 0
    n_removed = None
    while n_removed is None or n_removed > 0:
        removed = {
            (r, c)
            for r, line in enumerate(lines)
            for c, char in enumerate(line)
            if char == "@"
            and (r, c) not in ignore
            and neighboring_rolls(lines, r, c, ignore) < 4
        }
        n_removed = len(removed)
        cnt += n_removed
        ignore |= removed
    return cnt
