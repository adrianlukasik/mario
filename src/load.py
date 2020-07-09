import pygame

IMAGES_MARIO_PATH = '../images/mario/'


def load_image(path, name):
    return pygame.image.load(path + name)


def load_mario_image(name):
    return load_image(IMAGES_MARIO_PATH, name)
