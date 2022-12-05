import re
from collections import defaultdict, deque
from copy import deepcopy


def process_input(filename):
    stacks, moves = defaultdict(deque), []

    with open(filename) as f:
        head, body = f.read().split('\n\n')

    for line in head.split('\n'):
        for i, c in enumerate(line):
            if c.isalpha():
                stacks[i // 4 + 1].append(c)

    regex = r'^move (\d+) from (\d+) to (\d+)$'
    for line in body.split('\n'):
        try:
            moves.append(tuple(map(int, re.match(regex, line).groups())))
        except AttributeError:
            break

    return stacks, moves


def answer(stacks):
    return ''.join([s[0] for _, s in sorted(stacks.items(), key=lambda e: e[0])])


stacks, moves = process_input('day05.txt')
stacks_a, stacks_b = deepcopy(stacks), stacks

for count, source, destination in moves:
    src, dst = stacks_a[source], stacks_a[destination]
    for _ in range(count):
        dst.appendleft(src.popleft())

for count, source, destination in moves:
    src, dst = stacks_b[source], stacks_b[destination]
    crates = [src.popleft() for _ in range(count)]
    for c in reversed(crates):
        dst.appendleft(c)

print(answer(stacks_a), answer(stacks_b))
