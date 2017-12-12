from unittest import TestCase


class Graph:
    def __init__(self):
        self.vertices = {}

    def add_edges(self, vertex, neighbours):
        vertex = self.add_vertex(vertex)
        neighbours = map(self.add_vertex, neighbours)
        vertex.add_neighbours(neighbours)

    def add_vertex(self, name):
        existing = self.vertices.get(name, None)
        if not existing:
            existing = Vertex(name)
            self.vertices[name] = existing
        return existing

    def count_vertices_in_forest(self, vertex):
        return len(self.vertices[vertex].forest())

    def count_distinct_forests(self):
        remaining_vertices = set(self.vertices.values())
        groups = 0
        while len(remaining_vertices) > 0:
            vertex = remaining_vertices.pop()
            remaining_vertices -= vertex.forest()
            groups += 1
        return groups

    @staticmethod
    def of(data):
        lines = data.split('\n')
        g = Graph()
        for line in lines:
            if line.strip() == '':
                continue
            vertex, neighbours = line.split(' <-> ')

            g.add_edges(vertex, neighbours.split(', '))

        return g


class Vertex:
    def __init__(self, name):
        self.name = name
        self.neighbours = []

    def add_neighbour(self, neighbour):
        if neighbour not in self.neighbours:
            self.neighbours.append(neighbour)
        if self not in neighbour.neighbours:
            neighbour.neighbours.append(self)

    def add_neighbours(self, neighbours):
        for neighbour in neighbours:
            self.add_neighbour(neighbour)

    def forest(self, initial=None):
        if initial is None:
            initial = set()
        initial.add(self)

        remaining = set(self.neighbours) - initial
        for neighbour in remaining:
            neighbour.forest(initial)

        return initial


class TestDigitalPlumber(TestCase):
    def test_basic_graph(self):
        data = """
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5
        """

        self.assertEqual(6, Graph.of(data).count_vertices_in_forest('0'))

    def test_solutions(self):
        with open('graph.txt', 'r') as fin:
            data = fin.read()
            print('Solution part 1: %s' % Graph.of(data).count_vertices_in_forest('0'))
            print('Solution part 2: %s' % Graph.of(data).count_distinct_forests())
