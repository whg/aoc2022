import re
from collections import defaultdict, deque, namedtuple
from functools import partial
from math import floor, ceil
from multiprocessing import Pool

regex = re.compile(r'Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z ,]+)')
Valve = namedtuple('Valve', ('name', 'flow', 'connections'))


def parse(line):
    valve, rate, connections = re.match(regex, line).groups()
    return Valve(valve, int(rate), connections.split(', '))


def find_path(valves, start, end):
    visited = set()
    options = deque([start])
    costs = defaultdict(lambda: float('inf'))
    costs[start] = 0
    connections = {}

    while options:
        name = options.popleft()
        visited.add(name)
        for neighbour in valves[name].connections:
            if neighbour in visited:
                continue
            cost = costs[name] + 1
            if costs[neighbour] > cost:
                costs[neighbour] = cost
                options.append(neighbour)
                connections[neighbour] = name

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


def best_route(candidates, time_limit=30, n_best=9):
    scores = []

    def calc_pressure(time, flow, time_limit=30):
        return (time_limit - time) * flow

    def benefits(time, start, candidates, time_limit=30):
        def func(c):
            elapsed = time + paths[tuple(sorted((start, c)))] + 1
            return c, elapsed, calc_pressure(elapsed, valves[c].flow, time_limit)

        return list(map(func, candidates))

    def run(time, start, candidates, score, n_best=9):
        if len(candidates) == 0:
            scores.append(score)
        r = benefits(time, start, candidates)
        vs = sorted(r, key=lambda e: e[2], reverse=True)[:n_best]
        for name, t, pres in vs:
            if t < time_limit:
                added = calc_pressure(t, valves[name].flow, time_limit)
                run(t, name, candidates.difference({name}), score + added)
            else:
                scores.append(score)

    run(0, 'AA', set(candidates), 0)
    return max(scores)


def part_b_score(bins):
    return sum(map(partial(best_route, time_limit=26, n_best=5), bins))


def best_with_two(flowing):
    n_flowing = len(flowing)
    n_groups = 2**n_flowing
    done = set()
    groups = []

    for q in range(n_groups):
        qbin = bin(q)[2:]

        # don't have mirrors of a group
        if qbin[::-1] in done:
            continue

        ones = qbin.count('1')  # have the bins fairly equally matched
        if ones < floor(n_flowing / 2) or ones > ceil(n_flowing / 2):
            continue

        bins = ([], [])
        for i, valve in enumerate(flowing):
            bins[1 if (1 << i) & q else 0].append(valve)

        groups.append(bins)

    with Pool(6) as pool:
        scores = pool.map(part_b_score, groups)

    return max(scores)


valves = {v.name: v for v in map(parse, open('day16.txt').readlines())}
flowing = sorted([v.name for v in valves.values() if v.flow > 0], reverse=True)
paths = {}

for i, v in enumerate(flowing):
    paths[('AA', v)] = find_path(valves, 'AA', v)
    for w in flowing[i+1:]:
        paths[tuple(sorted((v, w)))] = find_path(valves, v, w)

part_a = best_route(flowing)
part_b = best_with_two(flowing)
print(part_a, part_b)
