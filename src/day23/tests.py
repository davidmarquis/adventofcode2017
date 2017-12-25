from day18.tests import Reference, Program, ProgramTerminated

mul_count = 0


class Day23InstructionSet:
    def run(self, program, operation, left, right=None):
        self._run(program, operation, Reference(left, program), Reference(right, program))

    def _run(self, program, operation, left, right):
        if operation == 'set':
            left.set(right.get())
        elif operation == 'sub':
            left.set(left.get() - right.get())
        elif operation == 'mul':
            global mul_count
            mul_count += 1
            left.set(left.get() * right.get())
        elif operation == 'jnz':
            if left.get() != 0:
                program.skip(right.get())


# Part 1
with open('instructions.txt', 'r') as fin:
    lines = fin.readlines()

try:
    program = Program(Day23InstructionSet(), lines)
    program.execute()
except ProgramTerminated:
    print('Solution part 1: %s' % mul_count)

# part 2
a = b = c = d = e = f = g = h = 0
a = 1
b = 79
b *= 100
b -= -100000
c = b
c -= -17000


def inner():
    global a, b, c, d, e, f, g, h
    g = d
    g *= e
    g -= b
    if g == 0:
        f = 0
    e -= -1
    g = e
    g -= b


def outer():
    global a, b, c, d, e, f, g, h
    e = 2
    inner()
    while g != 0:
        inner()

    d -= -1
    g = d
    g -= b


for b in range(b, c, 17):
    f, d  = 1, 2
    outer()
    while g != 0:
        outer()
        if f == 0:
            h -= -1
            print((e, d, h))
            break
    g = b
    g = c

print(h)

# Part 2 - we're counting non-prime numbers between two numbers, every 17 numbers!
h = 0
a = 1
start = 79 * 100 + 100000
end = start + 17000

for b in range(start, end + a, 17):
    for d in range(2, b):
        if b % d == 0:
            h += 1
            break
print('Solution part 2: %s' % h)
