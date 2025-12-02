from math import pow
from itertools import chain, count


def parse(data):
    ranges = data.strip().split(",")
    return [range_.split("-") for range_ in ranges]


def run(data, iterate_range):
    return sum(chain.from_iterable(iterate_range(a, b) for a, b in parse(data)))


def part1(data):
    def iterate_range(start, end):
        l = len(start)
        if l % 2 == 0:
            half = int(start[: l // 2])
        else:
            half = int(pow(10, l // 2))

        start = int(start)
        end = int(end)

        for inc in count():
            double = int(str(half + inc) * 2)
            if double < int(start):
                continue
            if double > end:
                break
            yield double

    return run(data, iterate_range)


def part2(data):
    def iterate_range(start, end):
        start = int(start)
        end = int(end)

        seen = set()

        for seed in range(1, int(str(end)[: len(str(end)) // 2 + 1]) + 1):
            for cnt in count(start=2):
                candidate = int(str(seed) * cnt)

                if candidate < start or candidate in seen:
                    continue
                if candidate > end:
                    break

                seen.add(candidate)

                yield candidate

    return run(data, iterate_range)
