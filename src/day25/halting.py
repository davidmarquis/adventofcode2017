import time

A, B, C, D, E, F = 0, 1, 2, 3, 4, 5
RIGHT = 1
LEFT = -1


# In state A:
#  If the current value is 0:
#  - Write the value 1.
#  - Move one slot to the right.
#  - Continue with state B.
#  If the current value is 1:
#  - Write the value 0.
#  - Move one slot to the left.
#  - Continue with state B.
def a(tape, cursor):
    if cursor in tape:
        tape.remove(cursor)
        return B, LEFT
    else:
        tape.add(cursor)
        return B, RIGHT


#  In state B:
#  If the current value is 0:
#  - Write the value 0.
#  - Move one slot to the right.
#  - Continue with state C.
#  If the current value is 1:
#  - Write the value 1.
#  - Move one slot to the left.
#  - Continue with state B.
def b(tape, cursor):
    if cursor in tape:
        return B, LEFT
    else:
        return C, RIGHT


#  In state C:
#  If the current value is 0:
#  - Write the value 1.
#  - Move one slot to the right.
#  - Continue with state D.
#  If the current value is 1:
#  - Write the value 0.
#  - Move one slot to the left.
#  - Continue with state A.
def c(tape, cursor):
    if cursor in tape:
        tape.remove(cursor)
        return A, LEFT
    else:
        tape.add(cursor)
        return D, RIGHT


#  In state D:
#  If the current value is 0:
#  - Write the value 1.
#  - Move one slot to the left.
#  - Continue with state E.
#  If the current value is 1:
#  - Write the value 1.
#  - Move one slot to the left.
#  - Continue with state F.
def d(tape, cursor):
    if cursor in tape:
        return F, LEFT
    else:
        tape.add(cursor)
        return E, LEFT


#  In state E:
#  If the current value is 0:
#  - Write the value 1.
#  - Move one slot to the left.
#  - Continue with state A.
#  If the current value is 1:
#  - Write the value 0.
#  - Move one slot to the left.
#  - Continue with state D.
def e(tape, cursor):
    if cursor in tape:
        tape.remove(cursor)
        return D, LEFT
    else:
        tape.add(cursor)
        return A, LEFT


#  In state F:
#  If the current value is 0:
#  - Write the value 1.
#  - Move one slot to the right.
#  - Continue with state A.
#  If the current value is 1:
#  - Write the value 1.
#  - Move one slot to the left.
#  - Continue with state E.
def f(tape, cursor):
    if cursor in tape:
        return E, LEFT
    else:
        tape.add(cursor)
        return A, RIGHT


def run(steps=1):
    tape = set()
    cursor = 0
    states = [a, b, c, d, e, f]

    start = time.time()
    # Begin in state A.
    state = A
    for _ in range(steps):
        state_func = states[state]
        state, movement = state_func(tape, cursor)
        cursor += movement

    print('Solution part 1: %s' % len(tape))
    print('Completed in %.2f sec' % (time.time() - start))


# Perform a diagnostic checksum after 12586542 steps.
run(12586542)