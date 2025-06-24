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

# Camera state
camera_pos = [0.0, 0.0, 7.0]  
yaw = -90.0
pitch = 0.0
sensitivity = 0.2
speed = 0.1

loadingworld = input('Import World Name:')

wdata = o_w.extmeta(loadingworld)

print(wdata)
print(o_w.getalldata(loadingworld))


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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    front = get_camera_front()
    target = [camera_pos[i] + front[i] for i in range(3)]
    gluLookAt(*camera_pos, *target, 0.0, 1.0, 0.0)

    render_world.render_world(  o_w.getalldata  (loadingworld,chunk = [math.floor(camera_pos[0]/16),math.floor(camera_pos[2]/16)]))

def handle_keyboard():
    print(get_camera_front()) 
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

def main():
    global yaw, pitch, camera_pos, texture_id

    pygame.init()
    screen = pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    pygame.display.set_caption(wdata[0])

    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (800 / 600), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.1, 0.1, 0.1, 1.0)

    texture_id = load_texture('Textures/default.jpg')

    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60)

        handle_keyboard()

        draw_scene()  # <-- draws every frame
        pygame.display.flip()  # <-- updates screen

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
