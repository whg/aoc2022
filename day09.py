lines = open('day09.txt').readlines()


def step(head, tail):
    (hx, hy), (tx, ty) = head, tail
    dx, dy = hx - tx, hy - ty
    if abs(dx) > 1 or abs(dy) > 1:
        tail = tx + max(min(dx, 1), -1), ty + max(min(dy, 1), -1)
    return tail


def move(rope, direction):
    dx, dy = 0, 0
    if direction == 'U':
        dy = 1
    elif direction == 'D':
        dy = -1
    elif direction == 'R':
        dx = 1
    elif direction == 'L':
        dx = -1

    output = rope[:]
    output[0] = output[0][0] + dx, output[0][1] + dy

    for i in range(len(output) - 1):
        head, tail = output[i], output[i+1]
        output[i+1] = step(head, tail)
    return output


def run(n):
    rope = [(0, 0)] * n
    tail_positions = {rope[-1]}
    for line in lines:
        direction, n = line.split()
        for _ in range(int(n)):
            rope = move(rope, direction)
            tail_positions.add(rope[-1])
    return len(tail_positions)


print(run(2), run(10))