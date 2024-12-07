import sys
import os

# Global Variables
instruction_Cache = []  # Cache structure for instructions
data_Cache = []  # Cache structure for data
instruction_Cache_Stats = {'accesses': 0, 'hits': 0, 'misses': 0}  # Statistics for instruction cache
data_Cache_Stats = {'accesses': 0, 'hits': 0, 'misses': 0}  # Statistics for data cache
cache_Config = {
    'total_Size': 0,      # Cache size (in bytes per cache)
    'line_Size': 0,       # Line size (in bytes)
    'access_Time': 0,     # Cache access time (in cycles)
    'memory_Access_Time': 0,  # Memory access time (in cycles)
    'num_Lines': 0,       # Total number of lines in each cache
    'address_Bits': 0     # Number of bits in memory addressing
}


def initialize_Caches(total_Size, line_Size, access_Time, memory_Access_Time, address_Bits):
    global instruction_Cache, data_Cache, cache_Config, instruction_Cache_Stats, data_Cache_Stats

    # Validate and set cache configuration
    cache_Config['total_Size'] = total_Size
    cache_Config['line_Size'] = line_Size
    cache_Config['access_Time'] = access_Time
    cache_Config['memory_Access_Time'] = memory_Access_Time
    cache_Config['num_Lines'] = total_Size // line_Size
    cache_Config['address_Bits'] = address_Bits

    # Reset statistics
    instruction_Cache_Stats = {'accesses': 0, 'hits': 0, 'misses': 0}
    data_Cache_Stats = {'accesses': 0, 'hits': 0, 'misses': 0}

    # Initialize instruction and data caches with default values (valid=0, tag=None)
    instruction_Cache = [{'valid': 0, 'tag': None} for _ in range(cache_Config['num_Lines'])]
    data_Cache = [{'valid': 0, 'tag': None} for _ in range(cache_Config['num_Lines'])]

    print(f"\nInstruction and Data Caches initialized with {cache_Config['num_Lines']} lines each.")
    print(f"Memory Address Bits: {address_Bits}, Memory Access Time: {memory_Access_Time} cycles")
    print(f"Cache Size: {total_Size} bytes, Line Size: {line_Size} bytes, Cache Access Time: {access_Time} cycles\n")


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

    print(f"Address: {address}, Index: {index}, Tag: {tag}, Result: {result}")
    print(f"  Total Accesses: {stats['accesses']}, Hits: {stats['hits']}, Misses: {stats['misses']}\n")

    return index, tag, result


def calculate_AMAT(stats):
    if stats['accesses'] == 0:
        return 0
    miss_Ratio = stats['misses'] / stats['accesses']
    amat = (cache_Config['access_Time'] +
            miss_Ratio * cache_Config['memory_Access_Time'])
    return amat


def print_Final_Stats():
    # Final statistics for instruction cache
    if instruction_Cache_Stats['accesses'] > 0:
        instr_Hit_Ratio = instruction_Cache_Stats['hits'] / instruction_Cache_Stats['accesses']
        instr_Miss_Ratio = instruction_Cache_Stats['misses'] / instruction_Cache_Stats['accesses']
    else:
        instr_Hit_Ratio = 0
        instr_Miss_Ratio = 0
    instr_AMAT = calculate_AMAT(instruction_Cache_Stats)

    # Final statistics for data cache
    if data_Cache_Stats['accesses'] > 0:
        data_Hit_Ratio = data_Cache_Stats['hits'] / data_Cache_Stats['accesses']
        data_Miss_Ratio = data_Cache_Stats['misses'] / data_Cache_Stats['accesses']
    else:
        data_Hit_Ratio = 0
        data_Miss_Ratio = 0
    data_AMAT = calculate_AMAT(data_Cache_Stats)

    # Print final results
    print("\nFinal Simulation Results:")
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

    # Print final state of the caches
    print("\nFinal Cache States:")
    print("Instruction Cache State:")
    for i, line in enumerate(instruction_Cache):
        print(f"  Line {i}: Valid = {line['valid']}, Tag = {line['tag']}")
    print("\nData Cache State:")
    for i, line in enumerate(data_Cache):
        print(f"  Line {i}: Valid = {line['valid']}, Tag = {line['tag']}")


def simulate_Access_Sequences(instruction_Sequence, data_Sequence):
    print("\nStarting separate cache simulation...\n")

    # Simulate instruction cache accesses
    print("Instruction Cache Accesses:")
    for address in instruction_Sequence:
        access_Cache(address, instruction_Cache, instruction_Cache_Stats)

    # Simulate data cache accesses
    print("\nData Cache Accesses:")
    for address in data_Sequence:
        access_Cache(address, data_Cache, data_Cache_Stats)

    # Print final simulation results
    print_Final_Stats()


def is_binary_string(s):
    return all(c in '01' for c in s)


def read_sequence_from_file(filename, address_Bits):
    """
    Reads a comma-separated list of addresses from a file and returns them as a list of integers.
    Handles both binary and decimal addresses.
    """
    if not os.path.isfile(filename):
        print(f"File {filename} does not exist.")
        return []

    with open(filename, 'r') as f:
        content = f.read().strip()
    if not content:
        return []

    addresses = []
    for addr_str in content.split(','):
        addr_str = addr_str.strip()
        if not addr_str:
            continue

        # Check if binary
        if is_binary_string(addr_str):
            # Convert from binary
            val = int(addr_str, 2)
            if val >= 2**address_Bits:
                print(f"Address {addr_str} exceeds the allowed address bits ({address_Bits}).")
                continue
            addresses.append(val)
        else:
            # Decimal
            if addr_str.isdigit():
                val = int(addr_str)
                if val >= 2**address_Bits:
                    print(f"Address {val} exceeds the allowed address bits ({address_Bits}).")
                    continue
                addresses.append(val)
            else:
                print(f"Ignoring invalid address: {addr_str}")

    return addresses


def get_valid_int(prompt, valid_range=None, positive_only=False):
    """
    Utility function to repeatedly prompt the user until a valid integer is entered.
    If valid_range is provided as (min_val, max_val), the entered value must lie within this range.
    If positive_only is True, the value must be > 0.
    """
    while True:
        try:
            value = int(input(prompt).strip())
            if valid_range:
                if value < valid_range[0] or value > valid_range[1]:
                    print(f"Value must be between {valid_range[0]} and {valid_range[1]}. Please try again.")
                    continue
            if positive_only and value <= 0:
                print("Value must be a positive integer. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid integer. Please try again.")


def run_Program():
    """
    Terminal-based program for running test cases or loading from files.
    According to the PDF, the inputs must match exactly these names:
    1. The number of bits needed to address the memory (an integer between 16 and 40)
    2. The memory access time in cycles (an integer between 50 and 200)
    3. The total cache size S (in bytes)
    4. The cache line size L (in bytes)
    5. The number of cycles needed to access the cache (an integer between 1 and 10 clock cycles)
    """

    print("Welcome to the Cache Simulator!\n")

    # Matching exactly the PDF wording:
    address_Bits = get_valid_int("The number of bits needed to address the memory (an integer between 16 and 40): ", (16, 40))
    memory_Access_Time = get_valid_int("The memory access time in cycles (an integer between 50 and 200): ", (50, 200))
    total_Size = get_valid_int("The total cache size S (in bytes): ", positive_only=True)
    line_Size = get_valid_int("The cache line size L (in bytes): ", positive_only=True)
    cache_Access_Time = get_valid_int("The number of cycles needed to access the cache (an integer between 1 and 10 clock cycles): ", (1, 10))

    initialize_Caches(total_Size, line_Size, cache_Access_Time, memory_Access_Time, address_Bits)

    while True:
        print("\nCache Simulator Menu")
        print("====================")
        print("1. Test Case 1: Unique Addresses (No Hits)")
        print("2. Test Case 2: Repeated Addresses (High Hit Ratio)")
        print("3. Test Case 3: Mixed Access Pattern")
        print("4. Load sequences from file")
        print("5. Exit")
        choice = input("Select a test case (1-5): ").strip()

        if choice == "1":
            initialize_Caches(total_Size, line_Size, cache_Access_Time, memory_Access_Time, address_Bits)
            instruction_Sequence = [0, 16, 32, 48, 64, 128, 256]
            data_Sequence = [8, 24, 40, 56, 72, 136, 264]
            simulate_Access_Sequences(instruction_Sequence, data_Sequence)
        elif choice == "2":
            initialize_Caches(total_Size, line_Size, cache_Access_Time, memory_Access_Time, address_Bits)
            instruction_Sequence = [0, 16, 32, 0, 16, 32, 0, 16, 32]
            data_Sequence = [8, 24, 40, 8, 24, 40, 8, 24, 40]
            simulate_Access_Sequences(instruction_Sequence, data_Sequence)
        elif choice == "3":
            initialize_Caches(total_Size, line_Size, cache_Access_Time, memory_Access_Time, address_Bits)
            instruction_Sequence = [0, 16, 32, 48, 0, 64, 16, 128, 256]
            data_Sequence = [8, 24, 40, 56, 8, 72, 24, 136, 264]
            simulate_Access_Sequences(instruction_Sequence, data_Sequence)
        elif choice == "4":
            instruction_File = input("Enter the instruction addresses file name: ").strip()
            data_File = input("Enter the data addresses file name: ").strip()

            instruction_Sequence = read_sequence_from_file(instruction_File, address_Bits)
            data_Sequence = read_sequence_from_file(data_File, address_Bits)

            if not instruction_Sequence or not data_Sequence:
                print("Could not load sequences from file(s). Ensure files exist and have valid comma-separated addresses.")
            else:
                initialize_Caches(total_Size, line_Size, cache_Access_Time, memory_Access_Time, address_Bits)
                simulate_Access_Sequences(instruction_Sequence, data_Sequence)
        elif choice == "5":
            print("Exiting...")
            sys.exit(0)
        else:
            print("Invalid choice. Please select a valid test case (1-5).")


if __name__ == "__main__":
    run_Program()