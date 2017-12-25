
def create_components(lines):
    return tuple((tuple(map(int, line.rstrip().split('/'))) for line in lines))


def create_bridges(components, bridge=None, last_port=1, level=0):
    if bridge is None:
        bridge = [(0, 0)]

    remaining_components = set(set(components) - set(bridge))
    for comp in remaining_components:
        if comp in bridge:
            continue
        try:
            connect_port = comp.index(bridge[-1][last_port])
            sub_bridge = list(bridge)
            sub_bridge.append(comp)
            yield from create_bridges(components, sub_bridge, abs(connect_port - 1), level + 1)
        except ValueError:
            continue

    yield bridge


with open('components.txt', 'r') as fin:
    lines = fin.readlines()

bridges = create_bridges(create_components(lines))

max_length = 0
max_length_strength = 0
max_strength = 0
for bridge in bridges:
    length = len(bridge)
    strength = sum(sum(component) for component in bridge)
    if length > max_length:
        max_length = length
        max_length_strength = strength
    if strength > max_strength:
        max_strength = strength

print('Solution part 1: %s' % max_strength)
print('Solution part 2: %s' % max_length_strength)