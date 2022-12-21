from operator import add, sub, mul, truediv

operators = {'+': add, '-': sub, '*': mul, '/': truediv}


def parse(line):
    monkey, job = line.split(': ')
    try:
        return monkey, int(job)
    except ValueError:
        return monkey, tuple(job.split())


def run(nodes, monkey):
    job = nodes[monkey]
    if type(job) is int or type(job) is float:
        return job
    a, op, b = job
    return operators[op](run(nodes, a), run(nodes, b))


def part1(monkeys):
    return int(run(monkeys, 'root'))


def part2(monkeys):
    deps = {}
    for monkey, job in monkeys.items():
        if type(job) is tuple:
            a, _, b = job
            assert a not in deps
            assert b not in deps
            deps[a] = deps[b] = monkey

    # build the path back to the root from humn
    path = ['humn']
    while True:
        dep = deps[path[-1]]
        if dep == 'root':
            break
        path.append(dep)

    # build the nested formulas from the root to humn
    formulas = {}
    for monkey in path:
        job = monkeys[monkey]
        if type(job) is tuple:
            a, op, b = job
            if a in formulas:
                formula = formulas[a], op, run(monkeys, b)
            else:
                formula = run(monkeys, a), op, formulas[b]
        else:
            formula = monkey
        formulas[monkey] = formula

    last = path[-1]
    a, _, b = monkeys['root']
    to_match = run(monkeys, a if b == last else b)
    formula = formulas[last]

    while True:
        a, op, b = formula
        if type(a) is tuple or a == 'humn':
            if op == '+':
                to_match = to_match - b
            elif op == '-':
                to_match = to_match + b
            elif op == '*':
                to_match = to_match / b
            else:
                to_match = to_match * b
            formula = a
        else:
            if op == '+':
                to_match = to_match - a
            elif op == '-':
                to_match = a - to_match
            elif op == '*':
                to_match = to_match / a
            else:
                to_match = a / to_match
            formula = b

        if a == 'humn' or b == 'humn':
            break

    return int(to_match)


lines = list(map(parse, open('day21.txt').read().splitlines()))
monkeys = dict(lines)
print(part1(monkeys), part2(monkeys))
