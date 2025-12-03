import math


def joltage(bank, size):
    if not size:
        return 0
    for a in reversed(range(1, 10)):
        subbank = bank[: 1 - size] if size > 1 else bank
        idx = subbank.find(str(a))
        if idx == -1:
            continue

        return int(math.pow(10, size - 1)) * a + joltage(bank[idx + 1 :], size - 1)

    raise


def part1(lines):
    return sum(joltage(bank, 2) for bank in lines)


def part2(lines):
    return sum(joltage(bank, 12) for bank in lines)
