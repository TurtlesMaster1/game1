import time

def guide():
    return 'First Value: World Name. Second Value: Version. Additional Data, with its own description, will be returned after'

def extmeta(world_name):
    start_time = time.perf_counter()
    world_meta = []

    # Read file content safely and split lines once
    with open('Saves/' + world_name + '/.wmeta', 'r') as f:
        lines = f.read().splitlines()

    # Extract world name and version
    world_meta.append(lines[0])  # World name
    world_meta.append(lines[1])  # World Data start index
    world_meta.append(lines[4])  # Version or similar

    # Parse additional data between '!@#' markers
    current_index = 5
    if lines[current_index] != '!@#':
        raise Exception("Expected '!@#' marker not found where expected")

    current_index += 1
    while current_index < len(lines) and lines[current_index] != '!@#':
        world_meta.append(lines[current_index])
        current_index += 1

    # Final safety check
    if current_index >= len(lines) or lines[current_index] != '!@#':
        raise Exception("Missing closing '!@#' marker in world file")

    elapsed = time.perf_counter() - start_time
    print(f"World metadata loading took {elapsed*1000:.2f}ms")
    return world_meta

def getchunk(world_name, chunk):
    start_time = time.perf_counter()
    with open('Saves/' + world_name + '/' + str(chunk), 'r') as f:
        lines = f.read().splitlines()
    elapsed = time.perf_counter() - start_time
    print(f"Chunk {chunk} loading took {elapsed*1000:.2f}ms")
    return lines