lines = open('day10.txt').readlines()

x = 1
values = [x]

for line in lines:
    tokens = line.split()
    if tokens[0] == 'noop':
        values.append(x)
    elif tokens[0] == 'addx':
        values += [x] * 2
        x += int(tokens[1])

points = [20, 60, 100, 140, 180, 220]
print(sum([values[p] * p for p in points]))

w, h = 40, 6
display = [[' ' for _ in range(w)] for _ in range(h)]

for i, value in enumerate(values[1:]):
    x, y = i % w, (i // w) % h
    display[y][x] = '#' if abs(value - x) <= 1 else '.'

for row in display:
    print(''.join(row))
