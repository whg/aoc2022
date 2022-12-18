from collections import Counter, defaultdict, deque


def parse(line):
    return tuple(int(v) * 2 for v in line.split(','))


def get_faces(coord):
    d = (-1, 1)
    x, y, z = coord
    for dx in d:
        yield x + dx, y, z
    for dy in d:
        yield x, y + dy, z
    for dz in d:
        yield x, y, z + dz


adj = [(-2, 0, 0), (2, 0, 0), (0, -2, 0), (0, 2, 0), (0, 0, -2), (0, 0, 2)]
not_trapped, trapped = set(), set()


def get_out(p, minx, maxx, miny, maxy, minz, maxz):
    global not_trapped, trapped
    if p in coords:
        raise Exception()
    if p in not_trapped:
        return True
    if p in trapped:
        return False

    visited = set()
    to_visit = deque([p])
    output = False

    while len(to_visit) > 0:
        q = to_visit.pop()
        if q in visited:
            continue
        visited.add(q)
        if q in not_trapped:
            output = True
            break
        if q in trapped:
            output = False
            break

        x, y, z = q
        if x < minx or x > maxx or y < miny or y > maxy or z < minz or z > maxz:
            output = True
            break

        for dx, dy, dz in adj:
            r = x + dx, y + dy, z + dz
            if r not in coords:
                to_visit.append(r)

    if output:
        not_trapped |= visited
    else:
        trapped |= visited
    return output


coords = list(map(parse, open('day18.txt').readlines()))
faces = set()

for c in coords:
    for f in get_faces(c):
        if f in faces:
            faces.remove(f)
        else:
            faces.add(f)

x, y, z = zip(*coords)
minx, maxx = min(x), max(x)
miny, maxy = min(y), max(y)
minz, maxz = min(z), max(z)

for z in range(minz, maxz + 1, 2):
    for y in range(miny, maxy + 1, 2):
        for x in range(minx, maxx + 1, 2):
            p = x, y, z
            if p not in coords:
                get_out(p, minx, maxx, miny, maxy, minz, maxz)

trapped_sides = set()
for p in trapped:
    for f in get_faces(p):
        trapped_sides.add(f)

n_trapped = len([f for f in faces if f in trapped_sides])
print(len(faces), len(faces) - n_trapped)
