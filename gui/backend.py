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

    cache_Config['total_Size'] = total_Size
    cache_Config['line_Size'] = line_Size
    cache_Config['access_Time'] = access_Time
    cache_Config['memory_Access_Time'] = memory_Access_Time
    cache_Config['num_Lines'] = total_Size // line_Size

    instruction_Cache.clear()
    data_Cache.clear()

    instruction_Cache.extend([{'valid': 0, 'tag': None} for _ in range(cache_Config['num_Lines'])])
    data_Cache.extend([{'valid': 0, 'tag': None} for _ in range(cache_Config['num_Lines'])])

    output(f"Instruction and Data Caches initialized with {cache_Config['num_Lines']} lines each.\n"
           f"Memory Access Time: {memory_Access_Time} cycles, Cache Access Time: {access_Time} cycles\n")


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
    amat = cache_Config['access_Time'] + miss_Ratio * cache_Config['memory_Access_Time']
    return amat


def preprocess_sequence_decimal(sequence):
    """Convert a string of decimal addresses into a list of integers."""
    if isinstance(sequence, list):  # If it's a list, join it into a string
        sequence = ",".join(map(str, sequence))  # Convert each item to a string
    return [int(address.strip()) for address in sequence.replace("\n", ",").split(",") if address.strip().isdigit()]


def preprocess_sequence_binary(sequence):
    """Convert a string of binary addresses into a list of integers."""
    if isinstance(sequence, list):  # If it's a list, join it into a string
        sequence = ",".join(map(str, sequence))  # Convert each item to a string

    binary_addresses = sequence.replace("\n", ",").split(",")
    validated_addresses = []
    for address in binary_addresses:
        address = address.strip()
        if not all(char in "01" for char in address):  # Check if the address is binary
            raise ValueError(f"Invalid binary address: {address}")
        validated_addresses.append(int(address, 2))  # Convert to integer

    return validated_addresses



def simulate_Access_Sequences(instruction_Sequence, data_Sequence, format_type):
    """
    Simulates separate instruction and data cache accesses.

    Parameters:
        instruction_Sequence (list): Instruction addresses.
        data_Sequence (list): Data addresses.
        format_type (str): Address format ("decimal" or "binary").
    """
    # Choose the preprocessing function based on the format type
    preprocess_sequence = preprocess_sequence_binary if format_type == "binary" else preprocess_sequence_decimal

    # Preprocess the input sequences
    instruction_Sequence = preprocess_sequence(instruction_Sequence)
    data_Sequence = preprocess_sequence(data_Sequence)

    output("Starting separate cache simulation...\n")

    # Simulate instruction cache accesses
    output("Instruction Cache Accesses:")
    for address in instruction_Sequence:
        index, tag, result = access_Cache(address, instruction_Cache, instruction_Cache_Stats)
        output(f"  Address: {address}, Index: {index}, Tag: {tag}, Result: {result}\n"
               f"    Total Accesses: {instruction_Cache_Stats['accesses']}, Hits: {instruction_Cache_Stats['hits']}, Misses: {instruction_Cache_Stats['misses']}\n")

    # Calculate and display hit and miss ratios for instruction cache
    if instruction_Cache_Stats['accesses'] > 0:
        instr_hit_ratio = instruction_Cache_Stats['hits'] / instruction_Cache_Stats['accesses']
        instr_miss_ratio = instruction_Cache_Stats['misses'] / instruction_Cache_Stats['accesses']
    else:
        instr_hit_ratio = instr_miss_ratio = 0


    # Simulate data cache accesses
    output("Data Cache Accesses:")
    for address in data_Sequence:
        index, tag, result = access_Cache(address, data_Cache, data_Cache_Stats)
        output(f"  Address: {address}, Index: {index}, Tag: {tag}, Result: {result}\n"
               f"    Total Accesses: {data_Cache_Stats['accesses']}, Hits: {data_Cache_Stats['hits']}, Misses: {data_Cache_Stats['misses']}\n")

    # Calculate and display hit and miss ratios for data cache
    if data_Cache_Stats['accesses'] > 0:
        data_hit_ratio = data_Cache_Stats['hits'] / data_Cache_Stats['accesses']
        data_miss_ratio = data_Cache_Stats['misses'] / data_Cache_Stats['accesses']
    else:
        data_hit_ratio = data_miss_ratio = 0



    print_Final_Stats(data_hit_ratio, data_miss_ratio, instr_hit_ratio, instr_miss_ratio)


def print_Final_Stats(data_hit_ratio, data_miss_ratio, instr_hit_ratio, instr_miss_ratio):
    instr_AMAT = calculate_AMAT(instruction_Cache_Stats)
    data_AMAT = calculate_AMAT(data_Cache_Stats)

    output("\nFinal Simulation Results:\n")
    output("Instruction Cache:\n"
           f"  Total Accesses: {instruction_Cache_Stats['accesses']}\n"
           f"  Total Hits: {instruction_Cache_Stats['hits']}\n"
           f"  Total Misses: {instruction_Cache_Stats['misses']}\n"
           f"  Average Memory Access Time (AMAT): {instr_AMAT:.2f} cycles\n"
           f"\nInstruction Cache Hit Ratio: {instr_hit_ratio:.2f}\n"
           f"Instruction Cache Miss Ratio: {instr_miss_ratio:.2f}\n")

    output("Data Cache:\n"
           f"  Total Accesses: {data_Cache_Stats['accesses']}\n"
           f"  Total Hits: {data_Cache_Stats['hits']}\n"
           f"  Total Misses: {data_Cache_Stats['misses']}\n"
           f"  Average Memory Access Time (AMAT): {data_AMAT:.2f} cycles\n"
           f"\nData Cache Hit Ratio: {data_hit_ratio:.2f}\n"
           f"Data Cache Miss Ratio: {data_miss_ratio:.2f}\n")

    output("\nFinal Cache States:\n")
    output("Instruction Cache State:")
    for i, line in enumerate(instruction_Cache):
        output(f"  Line {i}: Valid = {line['valid']}, Tag = {line['tag']}\n")

    output("\nData Cache State:")
    for i, line in enumerate(data_Cache):
        output(f"  Line {i}: Valid = {line['valid']}, Tag = {line['tag']}\n")

def run_Program(total_Size, line_Size, access_Time, memory_Access_Time, instruction_Sequence, data_Sequence, output_to_gui, format_type="decimal"):
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
    simulate_Access_Sequences(instruction_Sequence, data_Sequence, format_type)