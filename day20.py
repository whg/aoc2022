from collections import deque


def step(d: deque, index, shift):
    d.rotate(-index)
    v = d.popleft()
    shift %= len(d)
    d.insert(shift, v)
    d.rotate(index)

    new_index = (index + shift) % (len(d) - 1)
    if new_index != 0 and shift != 0 and new_index < index:
        d.rotate(1)


def answer(numbers):
    start = numbers.index(0)
    return sum((numbers[(start + i) % len(numbers)] for i in [1000, 2000, 3000]))


def part_a(lines):
    ids, numbers = (deque(l) for l in zip(*enumerate(lines)))

    for i, shift in enumerate(lines):
        j = ids.index(i)
        step(numbers, j, shift)
        step(ids, j, shift)

    return answer(numbers)


def part_b(lines):
    mlines = [v * 811589153 for v in lines]
    ids, numbers = (deque(l) for l in zip(*enumerate(mlines)))

    for n in range(10):
        for i, shift in enumerate(mlines):
            j = ids.index(i)
            step(numbers, j, shift)
            step(ids, j, shift)

    return answer(numbers)


lines = list(map(int, open('day20.txt').read().splitlines()))
print(part_a(lines), part_b(lines))
