import importlib
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import o_w
import os
from Objects import tri
import render_world
import math 
from OpenGL.GL import glGetString, GL_RENDERER, GL_VENDOR, GL_VERSION
import numpy as np
from performance_monitor import perf_monitor, timer, start_timer, stop_timer, increment_frame, print_summary



# Camera state
camera_pos = [0.0, 260, 7.0]  # Move camera to Y=260 to see the world
yaw = -90.0
pitch = 0.0
sensitivity = 0.2
speed = 1

loadingworld = input('Import World Name:')

wdata = o_w.extmeta(loadingworld)

print(wdata)


def getcurrentchunk(worldname):
    with timer("chunk_loading"):
        chunk_coords = [abs(math.floor(camera_pos[0]/16)), abs(math.floor(camera_pos[2]/16))]
        try:
            chunk_data = o_w.getchunk(loadingworld, chunk_coords)
            return chunk_data
        except Exception as e:
            return []
    



    
    glColor3f(1.0, 1.0, 1.0)  # Reset color
    glEnable(GL_TEXTURE_2D)  # Re-enable texturing

def get_camera_front():
    front_x = math.cos(math.radians(yaw)) * math.cos(math.radians(pitch))
    front_y = math.sin(math.radians(pitch))
    front_z = math.sin(math.radians(yaw)) * math.cos(math.radians(pitch))
    length = math.sqrt(front_x**2 + front_y**2 + front_z**2)
    return [front_x / length, front_y / length, front_z / length]


def load_texture(path):
    texture_surface = pygame.image.load(path)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", True)
    width, height = texture_surface.get_rect().size

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    return tex_id


def draw_scene():
    with timer("frame_render"):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        front = get_camera_front()
        target = [camera_pos[i] + front[i] for i in range(3)]
        gluLookAt(*camera_pos, *target, 0.0, 1.0, 0.0)

        # Try to render world data
        try:
            world_data = getcurrentchunk(loadingworld)
            if world_data:
                with timer("world_rendering"):
                    render_world.render_world(world_data)
        except Exception as e:
            pass

def handle_keyboard():
    with timer("input_handling"):
        global camera_pos
        keys = pygame.key.get_pressed()

        front = get_camera_front()
        front_flat = [front[0], 0.0, front[2]]  # zero out vertical (y) movement
        length = math.sqrt(front_flat[0]**2 + front_flat[2]**2)
        front_flat = [f / length for f in front_flat]  # normalize

        right = [front_flat[2], 0, -front_flat[0]]  # perpendicular
        up = [0.0, 1.0, 0.0]

        if keys[K_w]:
            camera_pos = [camera_pos[i] + front_flat[i] * speed for i in range(3)]
        if keys[K_s]:
            camera_pos = [camera_pos[i] - front_flat[i] * speed for i in range(3)]
        if keys[K_a]:
            camera_pos = [camera_pos[i] + right[i] * speed for i in range(3)]
            
        if keys[K_d]:
            camera_pos = [camera_pos[i] - right[i] * speed for i in range(3)]
        if keys[K_SPACE]:
            camera_pos = [camera_pos[i] + up[i] * speed for i in range(3)]
        if keys[K_LSHIFT]:
            camera_pos = [camera_pos[i] - up[i] * speed for i in range(3)]

def render_performance_display(font, small_font, fps):
    """Render performance statistics on screen"""
    # Switch to 2D rendering for text
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, 800, 600, 0, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Disable depth testing for 2D text
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_TEXTURE_2D)
    
    # Get performance stats
    all_stats = perf_monitor.get_all_stats()
    top_ops = perf_monitor.get_top_operations(5)
    
    # Render background box
    glColor4f(0.0, 0.0, 0.0, 0.7)  # Semi-transparent black
    glBegin(GL_QUADS)
    glVertex2f(10, 10)
    glVertex2f(350, 10)
    glVertex2f(350, 200)
    glVertex2f(10, 200)
    glEnd()
    
    # Render text
    glColor3f(1.0, 1.0, 1.0)  # White text
    
    # FPS display
    fps_text = f"FPS: {int(fps)}"
    fps_surface = font.render(fps_text, True, (255, 255, 255))
    fps_texture = pygame.image.tostring(fps_surface, "RGBA", True)
    
    glEnable(GL_TEXTURE_2D)
    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, fps_surface.get_width(), fps_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, fps_texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    glBegin(GL_QUADS)
    glTexCoord2f(0, 1)
    glVertex2f(20, 20)
    glTexCoord2f(1, 1)
    glVertex2f(20 + fps_surface.get_width(), 20)
    glTexCoord2f(1, 0)
    glVertex2f(20 + fps_surface.get_width(), 20 + fps_surface.get_height())
    glTexCoord2f(0, 0)
    glVertex2f(20, 20 + fps_surface.get_height())
    glEnd()
    
    glDeleteTextures([tex_id])
    glDisable(GL_TEXTURE_2D)
    
    # Performance stats
    y_offset = 50
    for i, (name, stats) in enumerate(top_ops):
        if stats and stats['count'] > 0:
            text = f"{name}: {stats['average']*1000:.1f}ms avg ({stats['count']} calls)"
            text_surface = small_font.render(text, True, (255, 255, 255))
            text_texture = pygame.image.tostring(text_surface, "RGBA", True)
            
            glEnable(GL_TEXTURE_2D)
            tex_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, tex_id)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, text_surface.get_width(), text_surface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, text_texture)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            
            glBegin(GL_QUADS)
            glTexCoord2f(0, 1)
            glVertex2f(20, y_offset)
            glTexCoord2f(1, 1)
            glVertex2f(20 + text_surface.get_width(), y_offset)
            glTexCoord2f(1, 0)
            glVertex2f(20 + text_surface.get_width(), y_offset + text_surface.get_height())
            glTexCoord2f(0, 0)
            glVertex2f(20, y_offset + text_surface.get_height())
            glEnd()
            
            glDeleteTextures([tex_id])
            glDisable(GL_TEXTURE_2D)
            
            y_offset += 25
    
    # Restore 3D rendering
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

def main():
    global yaw, pitch, camera_pos, texture_id

    pygame.init()
    screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption(wdata[0])

    # Print OpenGL GPU info after context is created
    print("OpenGL Vendor:", glGetString(GL_VENDOR).decode())
    print("OpenGL Renderer:", glGetString(GL_RENDERER).decode())
    print("OpenGL Version:", glGetString(GL_VERSION).decode())

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (800 / 600), 0.1, 1000.0)  # Increase far plane

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.1, 0.1, 0.1, 1.0)  # Darker background

    texture_id = load_texture('Textures/default.jpg')

    clock = pygame.time.Clock()

    # Initialize font for FPS display
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 16)
    small_font = pygame.font.SysFont('Arial', 12)

    frame_count = 0
    last_perf_print = 0
    
    while True:
        with timer("total_frame"):
            dt = clock.tick(60)
            increment_frame()
            frame_count += 1

            handle_keyboard()
            draw_scene()

            # Print FPS and performance stats every 60 frames
            fps = clock.get_fps()
            if frame_count % 60 == 0:
                print(f"FPS: {int(fps)}")
                # Print performance summary every 300 frames (5 seconds at 60fps)
                if frame_count % 300 == 0:
                    print_summary()
                # Log performance data every 600 frames (10 seconds at 60fps)
                if frame_count % 600 == 0:
                    perf_monitor.log_performance()
            
            # Render performance display on screen
            render_performance_display(font, small_font, fps)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    return
                elif event.type == MOUSEMOTION:
                    xrel, yrel = event.rel
                    yaw += xrel * sensitivity
                    pitch -= yrel * sensitivity


if __name__ == "__main__":
    main()
