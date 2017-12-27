import time


def create_components(lines):
    return set(tuple(map(int, line.rstrip().split('/'))) for line in lines)


def create_bridges(components, used_components=None, previous_component=None, previous_connect_port=1):
    if used_components is None:
        used_components = set()
        previous_component = (0, 0)

    remaining_components = components - used_components
    for comp in remaining_components:
        if comp in used_components:
            continue
            
        previous_port_value = previous_component[previous_connect_port]
        connect_port = None
        if comp[0] == previous_port_value:
            connect_port = 0
        elif comp[1] == previous_port_value:
            connect_port = 1

        if connect_port is not None:
            yield from create_bridges(components, used_components.union({comp}), comp, abs(connect_port - 1))

    yield used_components


with open('components.txt', 'r') as fin:
    lines = fin.readlines()

start = time.time()

max_length = 0
max_length_strength = 0
max_strength = 0

for bridge in create_bridges(create_components(lines)):
    length = len(bridge)
    strength = sum(sum(component) for component in bridge)

    if length > max_length:
        max_length = length
        max_length_strength = strength

    if strength > max_strength:
        max_strength = strength

print('Solution part 1: %s' % max_strength)
print('Solution part 2: %s' % max_length_strength)
print('Total time: %.2f sec' % (time.time() - start))