from collections import defaultdict, deque
from functools import partial


def coord(lines, letter):
    y, line = [(y, l) for y, l in enumerate(lines) if letter in l][0]
    return line.index(letter), y


def path_length(graph, start, end):
    visited = set()
    options = deque([start])
    costs = defaultdict(lambda: float('inf'))
    costs[start] = 0
    connections = {}

    while options:
        coord = options.popleft()
        visited.add(coord)
        for neighbour in graph[coord]:
            if neighbour in visited:
                continue
            cost = costs[coord] + 1
            if costs[neighbour] > cost:
                costs[neighbour] = cost
                options.append(neighbour)
                connections[neighbour] = coord

    path = deque([end])
    while True:
        current = path[-1]
        if current == start:
            break
        try:
            path.append(connections[current])
        except KeyError:
            return None
    return len(path) - 1


lines = open('day12.txt').read().splitlines()
w, h = len(lines[0]), len(lines)
heights = [[ord(c) - ord('a') for c in row.replace('S', 'a').replace('E', 'z')] for row in lines]

graph = defaultdict(list)

for x, y in ((x, y) for x in range(w) for y in range(h)):
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        xx, yy = x + dx, y + dy
        inside = 0 <= xx < w and 0 <= yy < h
        if inside and heights[yy][xx] - heights[y][x] <= 1:
            graph[(x, y)].append((xx, yy))

start, end = map(partial(coord, lines), ('S', 'E'))
path_length = partial(path_length, graph, end=end)

a = path_length(start)
starts = [(x, y) for x in range(w) for y in range(h) if heights[y][x] == 0]
b = min(filter(None, map(path_length, starts)))
print(a, b)
