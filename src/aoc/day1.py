def adjust(pos, instruction):
    sign = 1 if instruction[0] == "R" else -1
    inc = int(instruction[1:])
    zeros = 0

    # don't count the initial zero if we're starting on 0 already and turning left
    if pos == 0 and instruction[0] == "L":
        zeros -= 1

    pos += sign * inc

    while not 0 <= pos < 100:
        pos -= sign * 100
        zeros += 1

    if pos == 0 and instruction[0] == "L":
        zeros += 1

    return pos, zeros


def part1(lines):
    pos = 50
    zeros = 0

    for instruction in lines:
        pos, _ = adjust(pos, instruction)
        if pos == 0:
            zeros += 1

    return zeros


def part2(lines):
    pos = 50
    zeros = 0

    for instruction in lines:
        pos, new_zeros = adjust(pos, instruction)
        zeros += new_zeros

    return zeros
