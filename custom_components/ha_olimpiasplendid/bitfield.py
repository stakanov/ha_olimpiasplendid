def read_bits(value, start, length):
    return (value >> start) & ((1 << length) - 1)

def write_bits(reg, start, length, val):
    mask = ((1 << length) - 1) << start
    return (reg & ~mask) | (val << start)

def write_bit(reg, bit, val):
    mask = 1 << bit
    return (reg & ~mask) | (val << bit)
