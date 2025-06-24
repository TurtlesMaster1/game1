import numpy as np
import os
import math
import shutil
from collections import defaultdict

input_path = "elevation_data.aaigrid"
output_dir = "tri_chunks"
zip_output = "tri_chunks.zip"
cellsize = 1
nodata_value = -32768

texture_thresholds = {
    "water.jpg": 0,
    "dirt.jpg": 10,
    "grass.jpg": 30,
    "default.jpg": 60,
}

def read_aaigrid(path):
    with open(path, 'r') as f:
        header = {}
        for _ in range(6):
            key, value = f.readline().split()
            header[key.lower()] = float(value)
        data = np.loadtxt(f)
    return header, data

def get_texture(h):
    if h <= texture_thresholds["water.jpg"]:
        return "water.jpg"
    elif h <= texture_thresholds["dirt.jpg"]:
        return "dirt.jpg"
    elif h <= texture_thresholds["grass.jpg"]:
        return "grass.jpg"
    elif h <= texture_thresholds["default.jpg"]:
        return "grass.jpg"
    else:
        return "default.jpg"

def to_chunk_coords(x, z):
    return (x // 16, z // 16)

header, elevation = read_aaigrid(input_path)
rows, cols = elevation.shape
chunk_data = defaultdict(list)

for y in range(rows - 1):
    for x in range(cols - 1):
        h1, h2 = elevation[y, x], elevation[y, x+1]
        h3, h4 = elevation[y+1, x], elevation[y+1, x+1]
        if any(h == nodata_value for h in [h1, h2, h3, h4]):
            continue
        x0, z0 = x, y
        tri1 = [[x0, h1, z0], [x0+1, h2, z0], [x0, h3, z0+1]]
        tri2 = [[x0, h3, z0+1], [x0+1, h2, z0], [x0+1, h4, z0+1]]
        tex1 = get_texture((h1 + h2 + h3) / 3)
        tex2 = get_texture((h3 + h2 + h4) / 3)
        chunk = to_chunk_coords(x0, z0)
        chunk_data[chunk].append((tex1, tri1))
        chunk_data[chunk].append((tex2, tri2))

if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
os.makedirs(output_dir)

for (cx, cz), tris in chunk_data.items():
    with open(f"{output_dir}/[{cx},{cz}]", "w") as f:
        for texture, verts in tris:
            f.write("tri\n")
            coords = [f"{vx},{vy},{vz}" for vx,vy,vz in verts]
            f.write(f'["{texture}", "{coords[0]}", "{coords[1]}", "{coords[2]}"]\n')

shutil.make_archive(output_dir, 'zip', output_dir)
print(f"Chunks saved and zipped as {zip_output}")
