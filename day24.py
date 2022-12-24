from collections import deque

bliz = {'>': (1, 0), '<': (-1, 0), 'v': (0, 1), '^': (0, -1)}
moves = list(bliz.values()) + [(0, 0)]

def run(start, end, minute):
    q = deque([(*start, minute)])

    searching = None
    visited = set()

    while len(q) > 0:

        current = x, y, m = q.popleft()

        if current in visited:
            continue
        visited.add(current)

        state = bliz_states.get(m)
        if state:
            bliz, bliz_pos = state
            # print('got state')
        else:
            bliz, _ = bliz_states[m - 1]
            for i, b in enumerate(bliz):
                xx, yy, d = b
                dx, dy = d
                bliz[i] = ((xx + dx) % width, (yy + dy) % height, d)

            bliz_pos = set((xx, yy) for xx, yy, _ in bliz)
            bliz_states[m] = bliz, bliz_pos

        for dx, dy in moves:
            p = xx, yy = x + dx, y + dy
            if (0 <= xx < width and 0 <= yy < height and p not in bliz_pos) or p == start:
                q.append((*p, m + 1))
            elif p == end:
                searching = m

        if searching is not None:
            break
        assert len(q) > 0

    return searching


lines = open('day24.txt').read().splitlines()
width, height = len(lines[0]) - 2, len(lines) - 2

start = lines[0].index('.') - 1, -1
end = lines[-1].index('.') - 1, height

blizzards = [(x - 1, y - 1, bliz[c]) for y, line in enumerate(lines) for x, c in enumerate(line) if c in bliz]
bliz_states = {0: (blizzards, set((x, y) for x, y, _ in blizzards))}

a = run(start, end, 1)
ba = run(end, start, a)
bb = run(start, end, ba)

print(a, bb)
