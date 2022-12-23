from collections import Counter

dirs = 'NSWE'


def parse(s):
    return [(x, y) for y, line in enumerate(s.split()) for x, c in enumerate(line) if c == '#']


def step(pos, d, elves):
    x, y = pos

    if d == 'N':
        if not any((x + dx, y - 1) in elves for dx in range(-1, 2)):
            return x, y - 1
    elif d == 'S':
        if not any((x + dx, y + 1) in elves for dx in range(-1, 2)):
            return x, y + 1
    elif d == 'W':
        if not any((x - 1, y + dy) in elves for dy in range(-1, 2)):
            return x - 1, y
    elif d == 'E':
        if not any((x + 1, y + dy) in elves for dy in range(-1, 2)):
            return x + 1, y


def next_pos(pos, fd, elves):
    start = dirs.index(fd)
    x, y = pos
    if any((x + dx, y + dy) in elves and (dx, dy) != (0, 0) for dx in range(-1, 2) for dy in range(-1, 2)):
        for i in range(len(dirs)):
            if np := step(pos, dirs[(start + i) % len(dirs)], elves):
                return np, True
    return pos, False


def run(elves, iterations):
    elves = elves[:]
    dir_index = 0

    for i in range(iterations):
        elves_set = set(elves)
        direction = dirs[dir_index]
        results = [next_pos(pos, direction, elves_set) for pos in elves]
        next_positions, moved = zip(*results)
        if any(moved):
            counts = Counter(next_positions)
            for i, np in enumerate(next_positions):
                if counts[np] == 1:
                    elves[i] = np
            dir_index = (dir_index + 1) % len(dirs)
        else:
            break
    return elves, i


def bounds(elves):
    bounds_x = (min(x for x, _ in elves), max(x for x, _ in elves))
    bounds_y = (min(y for _, y in elves), max(y for _, y in elves))
    return bounds_x, bounds_y


elves = parse(open('day23.txt').read())

a, _ = run(elves, 10)
bx, by = bounds(a)
print((bx[1] - bx[0] + 1) * (by[1] - by[0] + 1) - len(a), end=' ')

_, b = run(elves, int(1e6))
print(b + 1)
