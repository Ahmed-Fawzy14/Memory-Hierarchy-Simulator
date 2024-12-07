import sys
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

    # Validate and set cache configuration
    cache_Config['total_Size'] = total_Size
    cache_Config['line_Size'] = line_Size
    cache_Config['access_Time'] = access_Time
    cache_Config['memory_Access_Time'] = memory_Access_Time
    cache_Config['num_Lines'] = total_Size // line_Size

    # Initialize instruction and data caches with default values (valid=0, tag=None)
    instruction_Cache = [{'valid': 0, 'tag': None} for _ in range(cache_Config['num_Lines'])]
    data_Cache = [{'valid': 0, 'tag': None} for _ in range(cache_Config['num_Lines'])]

    output(f"Instruction and Data Caches initialized with {cache_Config['num_Lines']} lines each.")


def access_Cache(address, cache, stats):
  
    # Calculate cache index and tag
    line_Size = cache_Config['line_Size']
    num_Lines = cache_Config['num_Lines']
    index = (address // line_Size) % num_Lines
    tag = address // (line_Size * num_Lines)

    # Access cache line
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
    """
    Simulate separate instruction and data cache accesses.

    Parameters:
        instruction_Sequence (str): A string of instruction addresses separated by commas and/or newlines.
        data_Sequence (str): A string of data addresses separated by commas and/or newlines.
    """
    def preprocess_sequence(sequence):
        """Convert a string of addresses into a list of integers."""
        return [int(address.strip()) for address in sequence.replace("\n", ",").split(",") if address.strip().isdigit()]

    # Preprocess the input sequences
    instruction_Sequence = preprocess_sequence(instruction_Sequence)
    data_Sequence = preprocess_sequence(data_Sequence)

    output("Starting separate cache simulation...\n")

    # Simulate instruction cache accesses if sequence is non-empty
    if instruction_Sequence:
        output("Instruction Cache Accesses:")
        for address in instruction_Sequence:
            index, tag, result = access_Cache(address, instruction_Cache, instruction_Cache_Stats)
            output(f"Instruction Address: {address}, Index: {index}, Tag: {tag}, Result: {result}")
    else:
        output("No instruction addresses to simulate.")

    # Simulate data cache accesses if sequence is non-empty
    if data_Sequence:
        output("\nData Cache Accesses:")
        for address in data_Sequence:
            index, tag, result = access_Cache(address, data_Cache, data_Cache_Stats)
            output(f"Data Address: {address}, Index: {index}, Tag: {tag}, Result: {result}")
    else:
        output("\nNo data addresses to simulate.")

    # Final statistics for instruction cache
    if instruction_Sequence:
        instr_Hit_Ratio = instruction_Cache_Stats['hits'] / instruction_Cache_Stats['accesses']
        instr_Miss_Ratio = instruction_Cache_Stats['misses'] / instruction_Cache_Stats['accesses']
        instr_AMAT = calculate_AMAT(instruction_Cache_Stats)

        output("\nInstruction Cache:")
        output(f"  Total Accesses: {instruction_Cache_Stats['accesses']}")
        output(f"  Total Hits: {instruction_Cache_Stats['hits']}")
        output(f"  Total Misses: {instruction_Cache_Stats['misses']}")
        output(f"  Hit Ratio: {instr_Hit_Ratio:.2f}")
        output(f"  Miss Ratio: {instr_Miss_Ratio:.2f}")
        output(f"  Average Memory Access Time (AMAT): {instr_AMAT:.2f} cycles")

    # Final statistics for data cache
    if data_Sequence:
        data_Hit_Ratio = data_Cache_Stats['hits'] / data_Cache_Stats['accesses']
        data_Miss_Ratio = data_Cache_Stats['misses'] / data_Cache_Stats['accesses']
        data_AMAT = calculate_AMAT(data_Cache_Stats)

        output("\nData Cache:")
        output(f"  Total Accesses: {data_Cache_Stats['accesses']}")
        output(f"  Total Hits: {data_Cache_Stats['hits']}")
        output(f"  Total Misses: {data_Cache_Stats['misses']}")
        output(f"  Hit Ratio: {data_Hit_Ratio:.2f}")
        output(f"  Miss Ratio: {data_Miss_Ratio:.2f}")
        output(f"  Average Memory Access Time (AMAT): {data_AMAT:.2f} cycles")



def run_Program(total_Size, line_Size, access_Time, memory_Access_Time, instruction_Sequence, data_Sequence, output_to_gui):
    global output
    output = output_to_gui
    global instruction_Cache, data_Cache, instruction_Cache_Stats, data_Cache_Stats, cache_Config
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
    initialize_Caches(total_Size, line_Size, access_Time, memory_Access_Time)
    simulate_Access_Sequences(instruction_Sequence, data_Sequence)
