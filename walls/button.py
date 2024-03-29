import pygame
import random

tile = 16

class Button(pygame.sprite.Sprite):
    def __init__(self, position, lever, screen):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, tile, tile)
        self.color = (255, 0, 255)

        self.screen = screen

        self.lever = lever
        self.curr_hit = False
        self.is_on = False

        self.image1 = pygame.image.load("entities/sprites/button1.png")
        self.image2 = pygame.image.load("entities/sprites/button2.png")

        self.rect.topleft = position
        pygame.sprite.Group()

    def update(self, player):
        self.collision_update(player)

        if self.is_on:
            self.image = self.image2
        else:
            self.image = self.image1

        self.screen.blit(self.image, (self.rect.x - 4, self.rect.y))

    def collision_update(self, player):

        hit = pygame.Rect.colliderect(self.rect, player.rect)
        if not self.lever:
            if hit and not self.curr_hit:
                self.curr_hit = True
                self.is_on = True

            if not hit:
                self.curr_hit = False
                self.is_on = False
        else:
            if hit and not self.curr_hit:
                self.curr_hit = True
                self.is_on = not self.is_on

            if not hit:
                self.curr_hit = False






