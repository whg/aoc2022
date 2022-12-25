q = {k: v - 2 for v, k in enumerate('=-012')}

def snafu2dec(s):
    m, output = 1, 0
    for c in reversed(s):
        output += q[c] * m
        m *= 5
    return output


def dec2snafu(v):
    bits = []
    while v:
        b = v % 5
        if b == 4:
            bits.append('-')
            v += 1
        elif b == 3:
            bits.append('=')
            v += 2
        else:
            bits.append(str(b))
        v //= 5
    return ''.join(reversed(bits))


numbers = open('day25.txt').read().splitlines()
print(dec2snafu(sum(map(snafu2dec, numbers))))
