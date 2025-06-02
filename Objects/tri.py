import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import imp_wor

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

def render(params):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, load_texture('Textures/' + str(params[1])))

    glBegin(GL_TRIANGLES)
    glTexCoord2f(0.5, 1.0)
    glVertex3f(*params[2])

    glTexCoord2f(0.0, 0.0)
    glVertex3f(*params[3])

    glTexCoord2f(1.0, 0.0)
    glVertex3f(*params[4])
    glEnd()

    glDisable(GL_TEXTURE_2D)