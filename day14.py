def parse(line):
    output = set()
    points = list(map(eval, line.split('->')))
    for pair in zip(points, points[1:]):
        (ax, ay), (bx, by) = sorted(pair)
        for x in range(ax, bx + 1):
            for y in range(ay, by + 1):
                output.add((x, y))
    return output


def step(solid, floor):
    x, y = 500, 0
    options = ((0, 1), (-1, 1), (1, 1))
    while y < floor:
        for dx, dy in options:
            p = x + dx, y + dy
            if p not in solid and p[1] != floor:
                x, y = p
                break
        else:
            return x, y


lines = open('day14.txt').readlines()

rock = set().union(*map(parse, lines))
solid = set(rock)
abyss = max(map(lambda p: p[1], rock))
floor = abyss + 2

units_a = 0
sand = set()
while p := step(solid, floor):
    if p[1] > abyss:
        break
    solid.add(p)
    units_a += 1

solid = set(rock)
units_b = 0
while p := step(solid, floor):
    solid.add(p)
    units_b += 1
    if p[1] == 0:
        break

print(units_a, units_b)

# xs = list(map(lambda p: p[0], solid))
# for y in range(floor):
#     for x in range(min(xs), max(xs) + 1):
#         p = x, y
#         print('#' if p in rock else 'o' if p in solid else '+' if y == 0 and x == 500 else '.', end='')f
#     print()
