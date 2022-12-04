def intersection(line):
    (xs, xe), (ys, ye) = ((int(s) for s in p.split('-')) for p in line.split(','))
    x = set(range(xs, xe + 1))
    y = set(range(ys, ye + 1))
    return len(x.intersection(y)), min(len(x), len(y))

def a(line):
    li, lm = intersection(line)
    return li == lm

def b(line):
    li, _ = intersection(line)
    return li > 0

lines = open('day04.txt').readlines()
print(sum(map(a, lines)), sum(map(b, lines)))
