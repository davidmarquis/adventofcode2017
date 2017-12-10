import re
from collections import defaultdict
from unittest import TestCase


class Tree:
    def __init__(self):
        self.root = None
        self.nodes = {}

    def build_tree(self, programs):
        self.nodes = {program.name: program for program in programs}

        for node in self.nodes.values():
            for child in node.children:
                child.parent = node
        
        self.root = next((node for node in self.nodes.values() if node.parent is None))

    def deepest_unbalanced_node(self, node=None):
        if node is None:
            node = self.root

        if not node.is_balanced:
            for child in node.children:
                if not child.is_balanced:
                    return self.deepest_unbalanced_node(child)
            return node

    @staticmethod
    def from_lines(lines):
        tree = Tree()
        programs = []
        for line in lines:
            parsed = re.match(r'(?P<name>[a-z]+) \((?P<weight>[\d]+)\)( -> (?P<children>[a-z, ]+))?', line).groupdict()
            children = parsed.get('children')
            programs.append(ProgramNode(tree, parsed['name'], int(parsed['weight']), children.split(', ') if children else []))

        tree.build_tree(programs)
        return tree


class ProgramNode:
    def __init__(self, tree, name, weight, children):
        self.name = name
        self.weight = weight
        self._children = children

        self.tree = tree
        self.parent = None

    @property
    def children(self):
        return (self.tree.nodes[child] for child in self._children)

    @property
    def total_weight(self):
        return self.weight + sum([child.total_weight for child in self.children])

    @property
    def is_balanced(self):
        return len(set([child.total_weight for child in self.children])) <= 1


class TestUnbalancedPrograms(TestCase):
    def test_part1_single_level(self):
        tree = Tree.from_lines([
            'qgcmjz (87) -> skzkx, pzkofch',
            'skzkx (87)',
            'pzkofch (87)',
        ])

        self.assertEqual('qgcmjz', tree.root.name)

    def test_part1_multiple_levels(self):
        tree = Tree.from_lines([
            'qgcmjz (70) -> skzkx, asasa',
            'pzkofch (87) -> qgcmjz, sjask',
            'sjask (80)',
            'skzkx (87)',
            'asasa (87)',
        ])

        self.assertEqual('pzkofch', tree.root.name)

    def test_solution_part1(self):
        with open('programs.txt', 'r') as fin:
            tree = Tree.from_lines([line for line in fin.readlines()])
            print('Solution part 1: %s' % tree.root.name)

    def test_unbalanced_node(self):
        tree = Tree.from_lines([
            'pbga (66)',
            'xhth (57)',
            'ebii (61)',
            'havc (66)',
            'ktlj (57)',
            'fwft (72) -> ktlj, cntj, xhth',
            'qoyq (66)',
            'padx (45) -> pbga, havc, qoyq',
            'tknk (41) -> ugml, padx, fwft',
            'jptl (61)',
            'ugml (68) -> gyxo, ebii, jptl',
            'gyxo (61)',
            'cntj (57)',
        ])

        self.assertEqual('tknk', tree.deepest_unbalanced_node().name)

    def test_solution_part2(self):
        with open('programs.txt', 'r') as fin:
            tree = Tree.from_lines([line for line in fin.readlines()])
            node = tree.deepest_unbalanced_node()

            children_by_weight = defaultdict(list)
            for child in node.children:
                children_by_weight[child.total_weight].append(child)

            weights = sorted(children_by_weight.keys())
            self.assertEqual(len(weights), 2)
            diff = weights[0] - weights[1]

            culprit = None
            for weight, children in children_by_weight.items():
                if len(children) == 1:
                    culprit = children[0]

            print('Solution part 2: %s' % str(culprit.weight + diff))
