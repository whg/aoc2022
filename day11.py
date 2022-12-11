import re

regex = r'''Monkey (\d+):
  Starting items: ([\d, ]+)
  Operation: new = old ([\*\+]) (\w+)
  Test: divisible by (\d+)
    If true: throw to monkey (\d+)
    If false: throw to monkey (\d+)'''


class Monkey:
    def __init__(self, config):
        m = re.match(regex, config).groups()
        self.id = int(m[0])
        self.items = list(map(int, m[1].split(', ')))
        self.operator, self.operand = m[2], m[3]
        self.test = int(m[4])
        self.destination = {True: int(m[5]), False: int(m[6])}
        self.count = 0

    def _process(self, old):
        return eval(f'old {self.operator} {self.operand}')

    def run(self, monkeys, divisor, limit):
        for item in self.items:
            worry = self._process(item) // divisor
            d = self.destination[worry % self.test == 0]
            monkeys[d].items.append(worry % limit)
        self.count += len(self.items)
        self.items.clear()

    def __repr__(self):
        return f'Monkey {self.id} ({self.count}): {", ".join(map(str, self.items))}'


def run(configs, iterations, divisor):
    monkeys = list(map(Monkey, configs))

    limit = eval('*'.join([str(m.test) for m in monkeys]))

    for _ in range(iterations):
        for m in monkeys:
            m.run(monkeys, divisor=divisor, limit=limit)

    x, y, *_ = sorted([m.count for m in monkeys], reverse=True)
    return x * y


configs = open('day11.txt').read().split('\n\n')
print(run(configs, 20, 3), run(configs, 10000, 1))
