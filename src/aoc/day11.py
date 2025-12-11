def parse(lines):
    result = dict()
    for line in lines:
        source, *outputs = line.split()
        source = source.strip(":")
        result[source] = outputs
    return result


def part1(lines):
    edges = parse(lines)

    paths = 0
    queue = ["you"]
    while queue:
        node = queue.pop()
        outputs = edges[node]
        for output in outputs:
            if output == "out":
                paths += 1
            else:
                queue.append(output)

    return paths


def part2(lines):
    edges = parse(lines)

    paths = 0
    queue = [("svr", False, False)]
    while queue:
        node, saw_dac, saw_fft = queue.pop()
        outputs = edges[node]
        for output in outputs:
            if output == "out":
                if saw_dac and saw_fft:
                    paths += 1
            else:
                queue.append(
                    (output, saw_dac or output == "dac", saw_fft or output == "fft")
                )

    return paths
