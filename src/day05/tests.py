from unittest import TestCase


def exit_maze_part1(maze):
    return exit_maze(maze, adjust_by_one)


def exit_maze_part2(maze):
    return exit_maze(maze, adjust_conditional)


def exit_maze(maze, adjustmnent_func):
    idx = steps = 0
    while idx < len(maze):
        value = maze[idx]
        maze[idx] = adjustmnent_func(value)
        idx += value
        steps += 1
    return steps


def adjust_by_one(value):
    return value + 1


def adjust_conditional(value):
    return value - 1 if value >= 3 else value + 1


class TestMazeEscape(TestCase):
    def test_part1(self):
        self.assertEqual(5, exit_maze_part1([0, 3, 0, 1, -3]))

        with open('steps.txt', 'r') as fin:
            print('Solution part 1: %s' % exit_maze_part1([int(line) for line in fin.readlines()]))

    def test_part2(self):
        self.assertEqual(10, exit_maze_part2([0, 3, 0, 1, -3]))

        with open('steps.txt', 'r') as fin:
            print('Solution part 2: %s' % exit_maze_part2([int(line) for line in fin.readlines()]))
