lines = open('day08.txt').read().split()
rows = [[int(t) for t in line] for line in lines]
n_rows, n_cols = len(rows), len(rows[0])


def part_a():
    def visible(heights, reverse=False):
        indices = []
        highest = -1
        hs = reversed(heights) if reverse else heights
        for i, height in enumerate(hs):
            if height > highest:
                index = len(heights) - i - 1 if reverse else i
                indices.append(index)
            if height == 9:
                break
            highest = max(height, highest)
        return indices

    visible_coords = set()

    def add(xs, ys):
        visible_coords.update(zip(xs, ys))

    for r, row in enumerate(rows):
        row_indices = [r] * n_rows
        add(visible(row, False), row_indices)
        add(visible(row, True), row_indices)

    cols = [[row[c] for row in rows] for c in range(n_cols)]
    for c, col in enumerate(cols):
        col_indices = [c] * n_cols
        add(col_indices, visible(col, False))
        add(col_indices, visible(col, True))

    return len(visible_coords)


def part_b():
    def score(coord):
        col, row = coord
        height = rows[row][col]
        rv, lv, dv, uv = 0, 0, 0, 0
        for ci in range(col + 1, n_cols):
            rv += 1
            if rows[row][ci] >= height:
                break
        for ci in range(col - 1, -1, -1):
            lv += 1
            if rows[row][ci] >= height:
                break
        for ri in range(row + 1, n_rows):
            dv += 1
            if rows[ri][col] >= height:
                break
        for ri in range(row - 1, -1, -1):
            uv += 1
            if rows[ri][col] >= height:
                break
        return rv * lv * dv * uv

    coords = ((c, r) for c in range(n_cols) for r in range(n_rows))
    return max(map(score, coords))


print(part_a(), part_b())
