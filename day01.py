c = [sum(map(int, e.split())) for e in open('day01.txt').read().split('\n\n')]
print(max(c), sum(sorted(c)[-3:]))
