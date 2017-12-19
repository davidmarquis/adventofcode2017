from collections import defaultdict
from itertools import cycle
from unittest import TestCase


class Program:
    def __init__(self, instructions_set, lines, read_queue=None, write_queue=None, program_id=0):
        self.instructions_set = instructions_set
        self.lines = lines
        self.read_queue = read_queue
        self.write_queue = write_queue
        self.cursor = 0
        self.send_count = 0
        self.waiting = False
        self.registers = defaultdict(int)
        self.registers['p'] = program_id

    def __getitem__(self, register):
        return self.registers[register]

    def __setitem__(self, key, value):
        self.registers[key] = value

    def execute(self):
        try:
            while True:
                self.run(self.lines[self.cursor])
                if self.waiting:
                    break
                self.cursor += 1
        except IndexError:
            raise ProgramTerminated()

    def run(self, instruction):
        parts = instruction.split()
        self.instructions_set.run(self, *parts)

    def is_waiting(self):
        return self.waiting and len(self.read_queue) == 0

    def send(self, value):
        self.send_count += 1
        self.write_queue.append(value)

    def receive(self):
        self.waiting = False
        try:
            return self.read_queue.pop(0)
        except IndexError:
            self.waiting = True
            return None

    def skip(self, count):
        self.cursor += count - 1


class CommunicatingInstructionSet:
    def run(self, program, operation, left, right=None):
        self._run(program, operation, Reference(left, program), Reference(right, program))

    def _run(self, program, operation, left, right):
        if operation == 'set':
            left.set(right.get())
        elif operation == 'add':
            left.set(left.get() + right.get())
        elif operation == 'mul':
            left.set(left.get() * right.get())
        elif operation == 'mod':
            left.set(left.get() % right.get())
        elif operation == 'jgz':
            if left.get() > 0:
                program.skip(right.get())
        elif operation == 'rcv':
            received = program.receive()
            if received:
                left.set(received)
        elif operation == 'snd':
            program.send(left.get())


class MusicalInstructionSet(CommunicatingInstructionSet):
    def __init__(self):
        self.sounds_played = []

    def _run(self, program, operation, left, right):
        if operation == 'snd':
            self.sounds_played.append(left.get())
        elif operation == 'rcv':
            raise ProgramTerminated()
        else:
            super()._run(program, operation, left, right)


class Reference(object):
    def __init__(self, ref, memory):
        self.ref = ref
        self.memory = memory

    def get(self):
        try:
            return int(self.ref)
        except:
            return self.memory[self.ref]

    def set(self, value):
        self.memory[self.ref] = value
    

class ProgramTerminated(Exception):
    pass


class TestCpu(TestCase):
    def test_simple_instructions(self):
        lines = [
            'set a 1',
            'add a 2',
            'mul a a',
            'mod a 5',
            'snd a',
            'set a 0',
            'rcv a',
            'jgz a -1',
            'set a 1',
            'jgz a -2',
        ]

        music = MusicalInstructionSet()
        program = Program(music, lines)

        try:
            program.execute()
            self.fail('Should have terminated')
        except ProgramTerminated:
            self.assertEqual(4, music.sounds_played[-1])

    def test_solution_part1(self):
        with open('instructions.txt', 'r') as fin:
            lines = fin.readlines()

        music = MusicalInstructionSet()
        program = Program(music, lines)

        try:
            program.execute()
        except ProgramTerminated:
            print('Solution part 1: %s' % music.sounds_played[-1])

    def test_simple_concurrency(self):
        lines = [
            'snd 1',
            'snd 2',
            'snd p',
            'rcv a',
            'rcv b',
            'rcv c',
            'rcv d',
        ]

        programs = self._create_programs(lines)

        try:
            self._run_programs(programs)
            self.fail('Should have terminated')
        except ProgramTerminated:
            self.assertEqual(3, programs[0].send_count)
            self.assertEqual(3, programs[1].send_count)

    def test_solution_part2(self):
        with open('instructions.txt', 'r') as fin:
            lines = fin.readlines()

        programs = self._create_programs(lines)

        try:
            self._run_programs(programs)
        except ProgramTerminated:
            print("Solution part 2: %s" % programs[1].send_count)

    @staticmethod
    def _create_programs(instructions):
        queue0 = []
        queue1 = []

        program0 = Program(CommunicatingInstructionSet(), instructions, read_queue=queue0, write_queue=queue1, program_id=0)
        program1 = Program(CommunicatingInstructionSet(), instructions, read_queue=queue1, write_queue=queue0, program_id=1)

        return program0, program1

    @staticmethod
    def _run_programs(programs):
        for program in cycle(programs):
            program.execute()
            if all(p.is_waiting() for p in programs):
                raise ProgramTerminated()