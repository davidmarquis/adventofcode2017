from collections import Counter
from unittest import TestCase


def add(a, b):
    return a[0] + b[0], a[1] + b[1], a[2] + b[2]


class Particle:
    def __init__(self, id, p, v, a):
        self.id = id
        self.p = p
        self.v = v
        self.a = a

    def tick(self):
        self.v = add(self.v, self.a)
        self.p = add(self.p, self.v)

    @property
    def distance(self):
        return sum(map(abs, self.p))


class ParticlesSystem:
    def __init__(self, particles):
        self.particles = particles

    def tick(self):
        for p in self.particles:
            p.tick()

    def remove_collisions(self):
        collisions = set(p for p, count in Counter([particle.p for particle in self.particles]).items() if count > 1)
        if collisions:
            self.particles = [particle for particle in self.particles if particle.p not in collisions]

    def particle_closest_from_center(self):
        return min(self.particles, key=lambda p: p.distance)


def parse(particle_id, value):
    def to_coordinates(s):
        return tuple(map(int, s[s.index('<') + 1:s.index('>')].split(',')))

    return Particle(particle_id, *map(to_coordinates, value.split(', ')))


class TestParticleSwarm(TestCase):
    def test_tick_particle(self):
        p0 = Particle(0, (3, 0, 0), (2, 0, 0), (-1, 0, 0))
        p1 = Particle(1, (4, 0, 0), (0, 0, 0), (-2, 0, 0))
        system = ParticlesSystem([p0, p1])

        self.assertEqual(3, p0.distance)
        self.assertEqual(4, p1.distance)
        system.tick()
        self.assertEqual(4, p0.distance)
        self.assertEqual(2, p1.distance)

    def test_closest_particle(self):
        p0 = Particle(0, (3, 0, 0), (2, 0, 0), (-1, 0, 0))
        p1 = Particle(1, (4, 0, 0), (0, 0, 0), (-2, 0, 0))
        system = ParticlesSystem([p0, p1])

        for _ in range(3):
            system.tick()

        self.assertEqual(0, system.particle_closest_from_center().id)

    def test_parsing(self):
        value = 'p=<3,4,2>, v=<2,-3,-6>, a=<-1,182,-192>'
        particle = parse(123, value)

        self.assertEqual(123, particle.id)
        self.assertEqual((3, 4, 2), particle.p)
        self.assertEqual((2, -3, -6), particle.v)
        self.assertEqual((-1, 182, -192), particle.a)

    def test_solution_part1(self):
        with open('particles.txt', 'r') as fin:
            lines = fin.readlines()

        system = ParticlesSystem([parse(idx, line) for idx, line in enumerate(lines)])

        for _ in range(1000):
            system.tick()

        print('Solution part 1: %s' % system.particle_closest_from_center().id)

    def test_solution_part2(self):
        with open('particles.txt', 'r') as fin:
            lines = fin.readlines()

        system = ParticlesSystem([parse(idx, line) for idx, line in enumerate(lines)])

        for _ in range(1000):
            system.tick()
            system.remove_collisions()

        print('Solution part 2: %s' % len(system.particles))