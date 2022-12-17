shapes_str = '''####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
'''


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y


class Shape:
    def __init__(self, points):
        self.points = points
        self.left_index = self.points.index(min(self.points, key=lambda p: p.x))
        self.right_index = self.points.index(max(self.points, key=lambda p: p.x))
        self.bottom_index = self.points.index(min(self.points, key=lambda p: p.y))
        self.top_index = self.points.index(max(self.points, key=lambda p: p.y))

    @classmethod
    def from_str(cls, s):
        lines = s.split()
        points = [Point(x, len(lines) - y - 1) for y, line in enumerate(lines)
                  for x, c in enumerate(line) if c == '#']
        return Shape(points)


class Chamber:
    def __init__(self, jets, width=7):
        self.width = width
        self.filled = set()
        self.jets = jets.strip()
        self._jet_index = len(self.jets) - 1
        self.bottom = -1

    def _bottom(self):
        if len(self.filled) == 0:
            return 0
        return max(self.filled, key=lambda e: e.y).y + 1

    @property
    def next_jet(self):
        self._jet_index = (self._jet_index + 1) % len(self.jets)
        return 1 if self.jets[self._jet_index] == '>' else -1

    def can_push(self, points, shape, direction):
        if direction == 1 and points[shape.right_index].x >= self.width - 1:
            return False
        if direction == -1 and points[shape.left_index].x <= 0:
            return False
        for p in points:
            if (p.x + direction, p.y) in self.filled:
                return False
        return True

    def can_drop(self, points, shape):
        if points[shape.bottom_index].y <= 0:
            return False
        for p in points:
            if (p.x, p.y - 1) in self.filled:
                return False
        return True

    def add(self, shape, move=True):
        bottom = self.bottom + shape.points[shape.bottom_index].y + 4
        offset = Point(2, bottom)

        points = [Point(v.x, v.y) for v in shape.points]
        for p in points:
            p.x += offset.x
            p.y += offset.y

        if move:
            while True:
                jet = self.next_jet
                if self.can_push(points, shape, jet):
                    for p in points:
                        p.x += jet

                if self.can_drop(points, shape):
                    for p in points:
                        p.y -= 1
                else:
                    break

        for p in points:
            self.filled.add((p.x, p.y))

        self.bottom = max(self.bottom, points[shape.top_index].y)

    def __repr__(self):
        top = max(self.filled, key=lambda e: e[1])[1]
        lines = []
        for y in range(top, -1, -1):
            l = ['#' if (x, y) in self.filled else '.' for x in range(self.width)]
            r = 1
            lines.append(f'|{"".join(l)}|')
        lines += [f'+{"-" * self.width}+']
        return '\n'.join(lines)


shapes = list(map(Shape.from_str, shapes_str.split('\n\n')))
jets = open('day17.txt').read().strip()
chamber = Chamber(jets)

N = 25000
sample_step = 1000
samples = []
for i in range(N):
    chamber.add(shapes[i % len(shapes)])
    if i + 1 == 2022:
        print(chamber.bottom + 1, end=' ')
    if i % sample_step == 0:
        samples.append(chamber.bottom + 1)

# we noticed that the increments start repeating after the first diff
diffs = [b - a for a, b in zip(samples, samples[1:])]
repeat = None
for i, e in enumerate(diffs[2:]):
    if e == diffs[1] and i > 2:
        repeat = i + 2
        break

count = 1000000000000
group = (repeat - 1) * sample_step
n = (count - sample_step) // group
total = diffs[0] + n * sum(diffs[1:repeat])
remaining = (count - sample_step - n * group) // sample_step
total += sum(diffs[1:remaining + 1])
print(total)
