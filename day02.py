def n(c):
    return (ord(c) - 64) % 23

def pa(a, b):
    return (n(b) - n(a) + 4) % 3 * 3 + n(b)

def pb(a, b):
    r = n(b) - 1
    return r * 3 + (n(a) + r + 4) % 3 + 1

lines = open('day02.txt').readlines()
print(*(sum([score(*l.split()) for l in lines]) for score in (pa, pb)))
