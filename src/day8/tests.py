from collections import defaultdict
from unittest import TestCase


class Cpu:
    def __init__(self):
        self.registers = defaultdict(int)

    def __getitem__(self, register):
        return self.registers[register]

    def __setitem__(self, key, value):
        self.registers[key] = value

    def highest_value(self):
        return max((value for register, value in self.registers.items()))


class Instruction(object):
    def __init__(self, operation, condition):
        self.operation = operation
        self.condition = condition

    def process(self, cpu):
        if self.condition.evaluate(cpu):
            self.operation.apply(cpu)

    @staticmethod
    def parse(line):
        parts = line.split()
        return Instruction(
            Operation(parts[0], parts[1], parts[2]),
            Condition(parts[4], parts[5], parts[6])
        )


class Operation(object):
    def __init__(self, register, operator, operand):
        self.register = register
        self.operator = 1 if operator == 'inc' else -1
        self.operand = int(operand)

    def apply(self, cpu):
        cpu[self.register] += self.operand * self.operator


class Condition(object):
    def __init__(self, left, operator, right):
        self.left = left
        self.predicate = self.predicate_for(operator)
        self.right = int(right)

    def evaluate(self, cpu):
        return self.predicate(cpu[self.left], self.right)

    @staticmethod
    def predicate_for(operator):
        return {
            '<': lambda a,b: a < b,
            '>': lambda a,b: a > b,
            '==': lambda a,b: a == b,
            '!=': lambda a,b: a != b,
            '<=': lambda a,b: a <= b,
            '>=': lambda a,b: a >= b,
        }[operator]


class TestCpu(TestCase):
    def test_simple_instructions(self):
        cpu = Cpu()

        Instruction.parse('b inc 5 if a < 1').process(cpu)
        Instruction.parse('a inc 2 if b == 5').process(cpu)

        self.assertEqual(5, cpu['b'])
        self.assertEqual(2, cpu['a'])

    def test_solutions(self):
        cpu = Cpu()

        highest_value_seen = 0
        with open('instructions.txt', 'r') as fin:
            for line in fin.readlines():
                Instruction.parse(line).process(cpu)

                highest_value = cpu.highest_value()
                if highest_value > highest_value_seen:
                    highest_value_seen = highest_value

        print('Solution part 1: ' + str(cpu.highest_value()))
        print('Solution part 2: ' + str(highest_value_seen))

