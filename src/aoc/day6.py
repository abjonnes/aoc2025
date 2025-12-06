from math import prod

OP_MAP = {"+": sum, "*": prod}


def part1(lines):
    parsed = [
        [int(x) if x.isnumeric() else OP_MAP[x] for x in line.split()] for line in lines
    ]
    return sum(ops[-1](ops[:-1]) for ops in zip(*parsed))


def part2(lines):
    edges = [idx for idx, char in enumerate(lines[-1]) if char != " "] + [
        len(lines[-1]) + 1
    ]
    return sum(
        OP_MAP[lines[-1][start]](
            int("".join(line[col] for line in lines[:-1] if line[col] != " "))
            for col in range(start, end - 1)
        )
        for start, end in zip(edges, edges[1:])
    )
