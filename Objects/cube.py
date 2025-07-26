import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

def load_texture(path):
    texture_surface = pygame.image.load(path)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", True)
    width, height = texture_surface.get_rect().size

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return tex_id

def parse_vertex(s):
    return tuple(map(float, s.split(',')))

def render(params):
    texture_name = params[0].strip().lower()

    if texture_name != "none":
        try:
            glEnable(GL_TEXTURE_2D)
            texture_path = 'Textures/' + texture_name
            texture_id = load_texture(texture_path)
            glBindTexture(GL_TEXTURE_2D, texture_id)

            glBegin(GL_TRIANGLES)
            glTexCoord2f(0.0, 1.0)
            glVertex3f(*parse_vertex(params[1]))
            glTexCoord2f(0.0, 0.0)
            glVertex3f(*parse_vertex(params[2]))
            glTexCoord2f(1.0, 0.0)
            glVertex3f(*parse_vertex(params[3]))
            glTexCoord2f(1.0, 1.0)
            glVertex3f(*parse_vertex(params[4]))
            glEnd()

            glDisable(GL_TEXTURE_2D)
        except Exception as e:
            pass
    else:
        # Use random color
        r, g, b = random.random(), random.random(), random.random()
        glColor3f(r, g, b)

        glBegin(GL_TRIANGLES)
        glVertex3f(*parse_vertex(params[1]))
        glVertex3f(*parse_vertex(params[2]))
        glVertex3f(*parse_vertex(params[3]))
        glEnd()

        glColor3f(1.0, 1.0, 1.0)
