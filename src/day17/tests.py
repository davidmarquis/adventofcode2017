step = 348

# part 1
position = 0
buffer = [0]

for idx in range(0, 2017):
    position = ((position + step) % (idx + 1)) + 1
    buffer.insert(position, idx + 1)

print('Solution part 1: %s' % buffer[position+1])


# part 2
second_value_last_seen = 0
for idx in range(0, 50000000):
    position = ((position + step) % (idx + 1)) + 1
    if position == 1:
        second_value_last_seen = idx + 1

print('Solution part 2: %s' % second_value_last_seen)


