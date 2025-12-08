from collections import Counter
from dataclasses import dataclass
from itertools import combinations
from math import prod


@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    @classmethod
    def parse(cls, line):
        x, y, z = [int(x) for x in line.split(",")]
        return cls(x, y, z)

    def distance(self, other):
        return (
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )


def run(lines, limit=None):
    points = [Point.parse(line) for line in lines]

    distances = sorted(
        ((a.distance(b), a, b) for a, b in combinations(points, 2)), reverse=True
    )

    components = {point: idx for idx, point in enumerate(points)}
    n_components = len(points)
    n_connections = 0

    a = b = None

    while (
        limit is None
        and n_components > 1
        or limit is not None
        and n_connections < limit
    ):
        n_connections += 1

        _, a, b = distances.pop()

        old_component, new_component = components[a], components[b]
        if old_component == new_component:
            continue

        n_components -= 1

        a_connections = [
            point
            for point, component in components.items()
            if component == old_component
        ]
        for point_to_update in a_connections:
            components[point_to_update] = new_component

    assert a and b

    return components, a, b


def part1(lines):
    components, _, _ = run(lines, limit=1000)
    counts = Counter(components.values())
    return prod(c for _, c in counts.most_common(3))


def part2(lines):
    _, a, b = run(lines)
    return a.x * b.x
