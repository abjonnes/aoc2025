from itertools import takewhile
from operator import attrgetter


def parse(lines):
    ranges = list()
    it = iter(lines)
    for range_ in takewhile(bool, it):
        a, b = range_.split("-")
        a, b = int(a), int(b)
        ranges.append(range(a, b + 1))

    items = [int(x) for x in it]

    return ranges, items


def part1(lines):
    ranges, items = parse(lines)

    return sum(any(item in range_ for range_ in ranges) for item in items)


def part2(lines):
    ranges, _ = parse(lines)

    ranges = sorted(ranges, key=attrgetter("start"))

    condensed = [ranges[0]]
    for range_ in ranges[1:]:
        if range_.start <= condensed[-1].stop:
            condensed[-1] = range(
                min(range_.start, condensed[-1].start),
                max(range_.stop, condensed[-1].stop),
            )
        else:
            condensed.append(range_)

    return sum(len(r) for r in condensed)
