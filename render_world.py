from Objects import tri
import ast
from OpenGL.GL import *
from OpenGL.GLU import *

def draw_debug_triangle():
    glColor3f(1.0, 0.0, 0.0)  # Bright red
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.9, -0.9)  # bottom-left
    glVertex2f(-0.7, -0.9)  # bottom-middle
    glVertex2f(-0.8, -0.7)  # middle-left
    glEnd()
    glColor3f(1.0, 1.0, 1.0)  # Reset color

def render_world(world_data_lines):
    parsed = []
    i = 0
    while i < len(world_data_lines) - 1:
        cmd = world_data_lines[i].strip()
        args_str = world_data_lines[i + 1].strip()
        try:
            args = ast.literal_eval(args_str)
            print(f"[OK] Parsed {cmd}: {args}")
            parsed.append([cmd, args])
        except Exception as e:
            print(f"[ERROR] Parsing failed at line {i}: {e}")
        i += 2

    for entry in parsed:
        print(f"[INFO] Dispatching {entry[0]}")
        if entry[0] == "tri":
            tri.render(entry[1])
        else:
            print(f"[WARN] Unknown command: {entry[0]}")

    draw_debug_triangle()
