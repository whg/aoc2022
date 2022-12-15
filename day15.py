import re


def parse(line):
    return tuple(map(int, re.findall(r'-?\d+', line)))


def manhattan(ax, ay, bx, by):
    return abs(ax - bx) + abs(ay - by)


def part_a(lines, ty):
    minx, maxx = 1e9, -1e9
    for sx, sy, bx, by in lines:
        dist = manhattan(sx, sy, bx, by)
        r = dist - abs(ty - sy)
        minx = min(sx - r, minx)
        maxx = max(sx + r, maxx)

    beacons = set()
    for _, _, bx, by in lines:
        if by == ty and minx <= bx <= maxx:
            beacons.add(bx)

    return maxx - minx - len(beacons) + 1


def part_b(lines, bounds):
    # the idea here is that any empty point will have the boundary of an area next to it
    # there are only two gradients for the lines that make up boundaries, (-1, 1)
    # so first we find the y intercept of these lines
    #  a/\b  line naming convention
    #  d\/c

    ma, mb, mc, md = set(), set(), set(), set()
    for sx, sy, bx, by in lines:
        dist = manhattan(sx, sy, bx, by)
        ma.add(sy - dist + sx)
        mb.add(sy - dist - sx)
        mc.add(sy + dist + sx)
        md.add(sy + dist - sx)

    # we look for a lines that are two above c lines, and the same for b and d
    # i.e. looking for a gap
    neg_gradients = [v + 1 for v in mc if v + 2 in ma]
    pos_gradients = [v + 1 for v in md if v + 2 in mb]
    position_candidates = set()

    # find the position of the all possible intersections
    for n in neg_gradients:
        for p in pos_gradients:
            x = (n - p) // 2
            y = x + p
            if 0 <= x <= bounds and 0 <= y <= bounds:
                position_candidates.add((x, x + p))

    # remove any candidates that are within the area of a sensor
    for x, y in set(position_candidates):
        if any((manhattan(sx, sy, x, y) < manhattan(sx, sy, bx, by) for sx, sy, bx, by in lines)):
            position_candidates.remove((x, y))

    assert len(position_candidates) == 1
    x, y = next(iter(position_candidates))
    return x * 4000000 + y


lines = list(map(parse, open('day15.txt').readlines()))
print(part_a(lines, 2000000), part_b(lines, 4000000))
