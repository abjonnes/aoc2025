from itertools import combinations, product
from dataclasses import dataclass
from PIL import Image


demo = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3""".split("\n")


@dataclass(order=True)
class Point:
    r: int
    c: int

    @classmethod
    def parse(cls, line):
        r, c = [int(x) for x in line.split(",")]
        return cls(r, c)


def part1(lines):
    # lines = demo
    points = [Point.parse(line) for line in lines]
    return max(
        (abs(p1.r - p2.r) + 1) * (abs(p1.c - p2.c) + 1)
        for p1, p2 in combinations(points, r=2)
    )


def part2(lines):
    # lines = demo
    points = [Point.parse(line) for line in lines]
    points.append(points[0])

    r_seq = sorted(set(p.r for p in points))
    c_seq = sorted(set(p.c for p in points))

    points = [Point(r_seq.index(p.r), c_seq.index(p.c)) for p in points]

    boundary = set()

    for p1, p2 in zip(points, points[1:]):
        assert p1.r == p2.r or p1.c == p2.c
        if p1.r == p2.r:
            low, high = sorted((p1.c, p2.c))
            boundary.update((p1.r, c) for c in range(low, high + 1))
        else:
            low, high = sorted((p1.r, p2.r))
            boundary.update((r, p1.c) for r in range(low, high + 1))

    min_r = min(p.r for p in points)

    shell = set()
    queue = [(min_r, min(c - 1 for r, c in boundary if r == min_r))]
    while queue:
        r, c = queue.pop()
        shell.add((r, c))

        for dr, dc in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            new_r, new_c = r + dr, c + dc
            if (
                (new_r, new_c) not in boundary
                and (new_r, new_c) not in shell
                and any(
                    (new_r + ddr, new_c + ddc) in boundary
                    for ddr, ddc in product(range(-1, 2), repeat=2)
                )
            ):
                queue.append((r + dr, c + dc))

    def check_row(r, c1, c2):
        for c in range(c1, c2 + 1):
            if (r, c) in shell:
                return False
        return True

    def check_col(c, r1, r2):
        for r in range(r1, r2 + 1):
            if (r, c) in shell:
                return False
        return True

    def valid(p1, p2):
        low_r, high_r = sorted((p1.r, p2.r))
        low_c, high_c = sorted((p1.c, p2.c))

        return (
            check_row(low_r, low_c, high_c)
            and check_row(high_r, low_c, high_c)
            and check_col(low_c, low_r, high_r)
            and check_col(high_c, low_r, high_r)
        )

    sized = sorted(
        (
            ((abs(r_seq[p1.r] - r_seq[p2.r]) + 1) * (abs(c_seq[p1.c] - c_seq[p2.c]) + 1), p1, p2)
            for p1, p2 in combinations(points, r=2)
        ),
        reverse=True,
    )

    size, p1, p2 = next((size, p1, p2) for size, p1, p2 in sized if valid(p1, p2))
    print(size, p1, p2)

    img = Image.new("RGB", (len(r_seq), len(c_seq)))
    white = (255, 255, 255)
    red = (255, 0, 0)
    for r, c in boundary:
        img.putpixel((r, c), white)

    for r, c in product(
        range(min(p1.r, p2.r), max(p1.r, p2.r) + 1),
        range(min(p1.c, p2.c), max(p1.c, p2.c) + 1),
    ):
        img.putpixel((r, c), red)

    img.save("image.png")
