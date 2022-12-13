from itertools import chain
from functools import cmp_to_key


def check(left, right):
    if len(left) == 0 and len(right) == 0:
        return None
    if len(left) == 0:
        return True
    if len(right) == 0:
        return False
    
    l, r, c = left[0], right[0], None
    if type(l) is int and type(r) is int:
        if l == r:
            c = check(left[1:], right[1:])
        else:
            return left < right
    elif type(l) is int:
        c = check([l], r)
    elif type(r) is int:
        c = check(l, [r])
    else:
        c = check(l, r)

    if c is None:
        return check(left[1:], right[1:])
    return c


parse = lambda s: tuple(map(eval, s.split()))
packet_pairs = list(map(parse, open('day13.txt').read().split('\n\n')))

a = sum([i + 1 for i, v in enumerate(packet_pairs) if check(*v)])

dividers = ([[2]], [[6]])
all_packets = list(chain(*packet_pairs, dividers))
key_func = cmp_to_key(lambda l, r: -1 if check(l, r) else 1)
s = sorted(all_packets, key=key_func)
x, y = (s.index(d) + 1 for d in dividers)

print(a, x * y)
