from Objects import tri
from Objects import cube
import ast
from OpenGL.GL import *
from OpenGL.GLU import *
import time

def draw_debug_triangle():
    glColor3f(1.0, 0.0, 0.0)  # Bright red
    glBegin(GL_TRIANGLES)
    glVertex3f(-0.9, -0.9, 0.0)  # Use 3D coordinates
    glVertex3f(-0.7, -0.9, 0.0)
    glVertex3f(-0.8, -0.7, 0.0)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)  # Reset color

def render_world(world_data_lines):
    start_time = time.perf_counter()
    rendered_count = 0
    
    for line in range(0, len(world_data_lines), 2):
        if line + 1 < len(world_data_lines) and world_data_lines[line] == "tri":
            try:
                # Parse the parameters string into a list
                params = ast.literal_eval(world_data_lines[line + 1])
                tri.render(params)
                rendered_count += 1
            except Exception as e:
                pass
    
    draw_debug_triangle()
    
    elapsed = time.perf_counter() - start_time
    if rendered_count > 0:
        print(f"Rendered {rendered_count} triangles in {elapsed*1000:.2f}ms ({elapsed*1000/rendered_count:.2f}ms per triangle)")


        
