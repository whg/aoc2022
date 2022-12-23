import re
from itertools import chain


def part_a(map_config):
    lines = [l.rstrip() for l in map_config.split('\n')]
    width, height = max(len(l) for l in lines), len(lines)
    map = [[None for x in range(width)] for y in range(height)]

    bounds_x = [(float('inf'), 0) for _ in range(height)]
    bounds_y = [(float('inf'), 0) for _ in range(width)]

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != ' ':
                map[y][x] = c == '.'
                minx, maxx = bounds_x[y]
                bounds_x[y] = (min(minx, x), max(maxx, x))
                miny, maxy = bounds_y[x]
                bounds_y[x] = (min(miny, y), max(maxy, y))

    tiles = set(chain(*[[(x, y) for x, c in enumerate(r) if c] for y, r in enumerate(map)]))
    next_tiles = {}
    for x, y in tiles:
        xp, xm, yp, ym = x + 1, x - 1, y + 1, y - 1
        bx, by = bounds_x[y], bounds_y[x]
        uc = (x, by[1] if ym < by[0] else ym)
        dc = (x, by[0] if yp > by[1] else yp)
        rc = (bx[0] if xp > bx[1] else xp, y)
        lc = (bx[1] if xm < bx[0] else xm, y)

        next_tiles[(x, y)] = {
            'U': uc if uc in tiles else (x, y),
            'D': dc if dc in tiles else (x, y),
            'R': rc if rc in tiles else (x, y),
            'L': lc if lc in tiles else (x, y)
        }

    return next_tiles


def run(start_x, path, next_tiles):
    dirs = 'RDLU'
    facing = dirs[0]
    position = (start_x, 0)

    for move in path:
        if move == 'R':
            facing = dirs[(dirs.index(facing) + 1) % len(dirs)]
        elif move == 'L':
            facing = dirs[(dirs.index(facing) - 1) % len(dirs)]
        else:
            for _ in range(move):
                n = next_tiles[position][facing]
                if len(n) == 2:
                    position = n
                else:
                    x, y, facing = n
                    position = (x, y)

    return password(position, dirs.index(facing))


def password(pos, facing_index):
    x, y = pos
    return (y + 1) * 1000 + (x + 1) * 4 + facing_index


def part_b(map_config):
    lines = [l.rstrip() for l in map_config.split('\n')]
    width, height = max(len(l) for l in lines), len(lines)
    s = max((width, height)) // 4
    w, h = width // s, height // s
    q = [[c != ' ' for c in line[::s]] + [False] * (4 - len(line) // s) for line in lines[::s]]
    q += [[False] * w] * (4 - len(q))

    def side_index(x, y):
        return y * 4 + x

    t = {
        12: {'L': (1, 'D'), 'D': (2, 'D'), 'R': (9, 'U')},
        9: {'D': (12, 'L'), 'R': (2, 'L')},
        8: {'L': (1, 'R'), 'U': (5, 'R')},
        5: {'L': (8, 'D'), 'R': (2, 'U')},
        2: {'D': (5, 'L'), 'R': (9, 'L'), 'U': (12, 'U')},
        1: {'L': (8, 'R'), 'U': (12, 'R')},
    }

    blocks = set()
    tiles = set()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '.':
                tiles.add((x, y))
            elif c == '#':
                blocks.add((x, y))

    next_tiles = {}
    options = [('R', 1, 0), ('L', -1, 0), ('U', 0, -1), ('D', 0, 1)]

    for x, y in tiles:
        o = {}
        for d, dx, dy in options:
            p = xx, yy = x + dx, y + dy
            if p in tiles:
                o[d] = (xx, yy)
                if (xx, yy) == (49, 163):
                    assert 0
            elif p in blocks:
                o[d] = (x, y)
            else:
                qx, qy = x // s, y // s
                si = side_index(qx, qy)
                ssi, dd = t[si][d]
                nx, ny = ssi % 4, ssi // 4
                opx, opy = qx * s, qy * s
                npx, npy = nx * s, ny * s
                rx, ry = x - opx, y - opy
                nex, ney = npx + s - 1, npy + s - 1

                if d == 'R':
                    if dd == 'L':
                        o[d] = (nex, ney - ry, dd)
                    elif dd == 'U':
                        o[d] = (npx + ry, ney, dd)
                    else:
                        raise Exception()
                elif d == 'L':
                    if dd == 'D':
                        o[d] = (npx + ry, npy, dd)
                    elif dd == 'R':
                        o[d] = (npx, ney - ry, dd)
                    else:
                        raise Exception()
                elif d == 'U':
                    if dd == 'R':
                        o[d] = (npx, npy + rx, dd)
                    elif dd == 'U':
                        o[d] = (npx + rx, ney, dd)
                    else:
                        raise Exception()
                elif d == 'D':
                    if dd == 'D':
                        o[d] = (npx + rx, npy, dd)
                    elif dd == 'L':
                        o[d] = (nex, npy + rx, dd)
                    else:
                        raise Exception()

            if (o[d][0], o[d][1]) in blocks:
                o[d] = (x, y)

        next_tiles[(x, y)] = o

    return next_tiles


m, ins = open('day22.txt').read().split('\n\n')
start_x = min(i for i, c in enumerate(m.split('\n')[0]) if c != ' ')
pairs = re.findall(r'(\d+)|([RL])', ins)
path = [int(i) if i.isdigit() else i for i in filter(None, chain(*pairs))]

print(run(start_x, path, part_a(m)), run(start_x, path, part_b(m)))
