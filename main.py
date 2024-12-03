# Global Variables
instruction_Cache = []  # Cache structure for instructions
data_Cache = []  # Cache structure for data
instruction_Cache_Stats = {'accesses': 0, 'hits': 0, 'misses': 0}  # Statistics for instruction cache
data_Cache_Stats = {'accesses': 0, 'hits': 0, 'misses': 0}  # Statistics for data cache
cache_Config = {
    'total_Size': 0,  # Cache size (in bytes per cache)
    'line_Size': 0,  # Line size (in bytes)
    'access_Time': 0,  # Cache access time (in cycles)
    'memory_Access_Time': 0,  # Memory access time (in cycles)
    'num_Lines': 0,  # Total number of lines in each cache
}  # Cache configuration


def initialize_Caches(total_Size, line_Size, access_Time, memory_Access_Time):
    global instruction_Cache, data_Cache, cache_Config

    cache_Config['total_Size'] = total_Size
    cache_Config['line_Size'] = line_Size
    cache_Config['access_Time'] = access_Time
    cache_Config['memory_Access_Time'] = memory_Access_Time
    cache_Config['num_Lines'] = total_Size // line_Size

    instruction_Cache = [{'valid': 0, 'tag': None} for _ in range(cache_Config['num_Lines'])]
    data_Cache = [{'valid': 0, 'tag': None} for _ in range(cache_Config['num_Lines'])]

    print(f"Instruction and Data Caches initialized with {cache_Config['num_Lines']} lines each.")


def access_Cache(address, cache, stats):

    line_Size = cache_Config['line_Size']
    num_Lines = cache_Config['num_Lines']
    index = (address // line_Size) % num_Lines
    tag = address // (line_Size * num_Lines)

    cache_Line = cache[index]
    stats['accesses'] += 1

    if cache_Line['valid'] and cache_Line['tag'] == tag:
        # Cache hit
        stats['hits'] += 1
        result = "HIT"
    else:
        # Cache miss
        stats['misses'] += 1
        cache_Line['valid'] = 1
        cache_Line['tag'] = tag
        result = "MISS"

    return index, tag, result


def calculate_AMAT(stats):

    hit_Ratio = stats['hits'] / stats['accesses']
    miss_Ratio = stats['misses'] / stats['accesses']
    amat = (cache_Config['access_Time'] +
            miss_Ratio * cache_Config['memory_Access_Time'])
    return amat


def simulate_Access_Sequences(instruction_Sequence, data_Sequence):

    print("Starting separate cache simulation...\n")

    # Simulate instruction cache accesses
    print("Instruction Cache Accesses:")
    for address in instruction_Sequence:
        index, tag, result = access_Cache(address, instruction_Cache, instruction_Cache_Stats)
        print(f"Instruction Address: {address}, Index: {index}, Tag: {tag}, Result: {result}")

    # Simulate data cache accesses
    print("\nData Cache Accesses:")
    for address in data_Sequence:
        index, tag, result = access_Cache(address, data_Cache, data_Cache_Stats)
        print(f"Data Address: {address}, Index: {index}, Tag: {tag}, Result: {result}")

    # Final statistics for instruction cache
    instr_Hit_Ratio = instruction_Cache_Stats['hits'] / instruction_Cache_Stats['accesses']
    instr_Miss_Ratio = instruction_Cache_Stats['misses'] / instruction_Cache_Stats['accesses']
    instr_AMAT = calculate_AMAT(instruction_Cache_Stats)

    # Final statistics for data cache
    data_Hit_Ratio = data_Cache_Stats['hits'] / data_Cache_Stats['accesses']
    data_Miss_Ratio = data_Cache_Stats['misses'] / data_Cache_Stats['accesses']
    data_AMAT = calculate_AMAT(data_Cache_Stats)

    # Print final results
    print("\nSimulation Results:")
    print("Instruction Cache:")
    print(f"  Total Accesses: {instruction_Cache_Stats['accesses']}")
    print(f"  Total Hits: {instruction_Cache_Stats['hits']}")
    print(f"  Total Misses: {instruction_Cache_Stats['misses']}")
    print(f"  Hit Ratio: {instr_Hit_Ratio:.2f}")
    print(f"  Miss Ratio: {instr_Miss_Ratio:.2f}")
    print(f"  Average Memory Access Time (AMAT): {instr_AMAT:.2f} cycles")

    print("\nData Cache:")
    print(f"  Total Accesses: {data_Cache_Stats['accesses']}")
    print(f"  Total Hits: {data_Cache_Stats['hits']}")
    print(f"  Total Misses: {data_Cache_Stats['misses']}")
    print(f"  Hit Ratio: {data_Hit_Ratio:.2f}")
    print(f"  Miss Ratio: {data_Miss_Ratio:.2f}")
    print(f"  Average Memory Access Time (AMAT): {data_AMAT:.2f} cycles")


# Cache Config: 256 bytes total per cache, 16 bytes per line, 1 cycle access time, 100 cycles memory time
initialize_Caches(total_Size=256, line_Size=16, access_Time=1, memory_Access_Time=100)

# Example Access Sequences
instruction_Sequence = [0, 16, 32, 48, 64, 128, 256]
data_Sequence = [8, 24, 40, 56, 72, 136, 264]
simulate_Access_Sequences(instruction_Sequence, data_Sequence)