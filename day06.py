def pa(line, n=4):
    for i in range(len(line) - n):
        if len(set(line[i:i+n])) == n:
            return i + n

line = open('day06.txt').read()
print(pa(line), pa(line, 14))
