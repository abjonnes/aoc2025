from functools import cache
from itertools import chain, combinations

import numpy as np
import scipy


def powerset(iterable):
    "Subsequences of the iterable from shortest to longest."
    # powerset([1,2,3]) → () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def parse(line):
    target, *buttons, joltage = line.split()
    target = tuple(int(x == "#") for x in target[1:-1])
    buttons = tuple(
        tuple(str(x) in button[1:-1].split(",") for x in range(len(target)))
        for button in buttons
    )
    joltage = tuple(int(x) for x in joltage[1:-1].split(","))
    return target, buttons, joltage


def part1(lines):
    @cache
    def operate(state, op):
        return tuple(a ^ b for a, b in zip(state, op))

    def count(line):
        target, buttons, _ = parse(line)
        for set_ in powerset(buttons):
            state = (0,) * len(target)
            for op in set_:
                state = operate(state, op)
            if state == target:
                return len(set_)
        raise Exception("shouldn't be here")

    return sum(count(line) for line in lines)


def part2(lines):
    def process(line):
        _, buttons, joltage = parse(line)

        a = np.array(buttons, dtype=int).T
        b = np.array([joltage]).T

        return round(
            scipy.optimize.linprog(
                [1] * len(buttons), A_eq=a, b_eq=b, integrality=3
            ).fun
        )

    return sum(process(line) for line in lines)
