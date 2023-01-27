from collections import deque


def parse(line):
    return tuple(int(v) * 2 for v in line.split(','))


def add(a, b):
    return tuple(av + bv for av, bv in zip(a, b))


coords = list(map(parse, open('day18.txt').readlines()))
sides = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)]
coord_faces = [{add(side, c) for side in sides} for c in coords]

open_faces = set()
for faces in coord_faces:
    open_faces = open_faces ^ faces

x, y, z = zip(*open_faces)
extremes = ((min(x), max(x)), (min(y), max(y)), (min(z), max(z)))
bounds = tuple((mn - 1, mx + 1) for mn, mx in extremes)

coords_to_visit = deque([tuple(mn for mn, _ in bounds)])
external_faces = set()
explored = set()

while len(coords_to_visit) > 0:
    coord = coords_to_visit.popleft()
    for side in sides:
        face = add(coord, side)
        for axis, v in enumerate(face):
            mn, mx = bounds[axis]
            if not mn <= v <= mx:
                break
        else:
            if face in open_faces:
                external_faces.add(face)
            else:
                next_coord = add(face, side)
                if next_coord not in explored:
                    coords_to_visit.append(next_coord)
                    explored.add(next_coord)

print(len(open_faces), len(external_faces))
