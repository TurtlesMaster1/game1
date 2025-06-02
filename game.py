import importlib
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import o_w
import os
from Objects import tri

# Camera state
camera_pos = [0.0, 0.0, 7.0]  # Start farther back so we can see the triangle
yaw = -90.0
pitch = 0.0
sensitivity = 0.2
speed = 0.1

loadingworld = input('Import World Name:')

wdata = o_w.extmeta(loadingworld)

print(wdata)


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

    tri.render()

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
    glClearColor(0.1, 0.1, 0.1, 1.0)

    texture_id = load_texture('Textures/default.jpg')  # Load texture once

    clock = pygame.time.Clock()

    while True:
        dt = clock.tick(60)

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
                pitch = max(-89.0, min(89.0, pitch))

        keys = pygame.key.get_pressed()
        front = get_camera_front()
        right = [
            math.sin(math.radians(yaw - 90)),
            0,
            math.cos(math.radians(yaw - 90))
        ]

        # Horizontal plane movement
        flat_front = [front[0], 0, front[2]]
        length = math.sqrt(flat_front[0]**2 + flat_front[2]**2)
        flat_front = [f / length for f in flat_front]

        if keys[K_w]:
            camera_pos[0] += flat_front[0] * speed
            camera_pos[2] += flat_front[2] * speed
        if keys[K_s]:
            camera_pos[0] -= flat_front[0] * speed
            camera_pos[2] -= flat_front[2] * speed
        if keys[K_a]:
            camera_pos = [camera_pos[i] - right[i] * speed for i in range(3)]
        if keys[K_d]:
            camera_pos = [camera_pos[i] + right[i] * speed for i in range(3)]
        if keys[K_SPACE]:
            camera_pos[1] += speed
        if keys[K_LSHIFT]:
            camera_pos[1] -= speed

        draw_scene()
        pygame.display.flip()

if __name__ == "__main__":
    main()