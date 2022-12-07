import re


class Node:
    def __init__(self, name, parent, size=0):
        self.name = name
        self.parent = parent
        self.size = size
        self.children = {}

    def add(self, size_or_dir, name):
        size = int(size_or_dir) if size_or_dir != 'dir' else 0
        self.children[name] = Node(name, self, size)


class Filesystem:
    def __init__(self):
        self.root = self.d = Node('/', None)

    def cd(self, dirname):
        if dirname == '..':
            self.d = self.d.parent
        else:
            self.d = self.d.children[dirname]

    def dir_sizes(self):
        output = []

        def sizes(node):
            if node.size > 0:
                return node.size
            dir_size = 0
            for n in node.children.values():
                dir_size += sizes(n)
            output.append(dir_size)
            return dir_size

        sizes(self.root)
        return output

    def part_a(self):
        sizes = self.dir_sizes()
        return sum([s for s in sizes if s < 100000])

    def part_b(self):
        sizes = self.dir_sizes()
        unused = 70000000 - sizes[-1]
        for size in sorted(sizes):
            if unused + size > 30000000:
                return size


lines = open('day07.txt').readlines()

fs = None
for line in lines:
    if match := re.match(r'^\$ cd ([/.\w]+)$', line):
        (path,) = match.groups()
        if path == '/':
            fs = Filesystem()
        else:
            fs.cd(path)
    elif match := re.match(r'^([\w]+) ([.\w]+)', line):
        size_or_dir, name = match.groups()
        fs.d.add(size_or_dir, name)

print(fs.part_a(), fs.part_b())
