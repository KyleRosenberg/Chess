import pygame
from Constants.Numbers import string_to_piece

class Sprite:

    def __init__(self, impath, type="board"):
        self.image = pygame.image.load(impath)
        self.type = type
        self.rect = pygame.Rect(0, 0, 100, 100)
        r = string_to_piece(type)
        self.area = self.image.get_rect() if r is None else r
        scale = self.rect.width/self.area.width
        self.area.x *= scale
        self.area.y *= scale
        self.area.width *= scale
        self.area.height *= scale
        if type == "board":
            self.image = pygame.transform.smoothscale(self.image, (self.rect.width, self.rect.height))
        else:
            self.image = pygame.transform.smoothscale(self.image, (self.rect.width*6, self.rect.height*2))

    def setPos(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def getPos(self):
        return self.rect.x, self.rect.y

    def setSize(self, w, h):
        self.rect.width = w
        self.rect.height = h
        scale = self.rect.width/self.area.width
        self.area.x *= scale
        self.area.y *= scale
        self.area.width *= scale
        self.area.height *= scale
        if self.type == "board":
            self.image = pygame.transform.smoothscale(self.image, (self.rect.width, self.rect.height))
        else:
            self.image = pygame.transform.smoothscale(self.image, (self.rect.width*6, self.rect.height*2))

    def setType(self, type):
        r = string_to_piece(type)
        self.area = self.image.get_rect() if r is None else r
        scale = self.rect.width/self.area.width
        self.area.x *= scale
        self.area.y *= scale
        self.area.width *= scale
        self.area.height *= scale

    def draw(self, screen):
        screen.blit(self.image, self.rect, self.area)
