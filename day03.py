def score(c):
    offset = 27 - ord('A') if c.isupper() else 1 - ord('a')
    return ord(c) + offset

def a(line):
    h = len(line) // 2
    first, second = set(line[:h]), set(line[h:])
    in_both = next(iter(first.intersection(second)))
    return score(in_both)

def b(group):
    x, y, z = (set(line.strip()) for line in group)
    in_all = next(iter(x.intersection(y).intersection(z)))
    return score(in_all)

lines = open('day03.txt').readlines()
print(sum(map(a, lines)), end=' ')
print(sum(map(b, zip(lines[::3], lines[1::3], lines[2::3]))))
