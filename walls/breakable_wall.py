import pygame

tile = 16

class Breakable_Wall(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, tile, tile)

        self.buffer = 2
        self.buffer_rect = pygame.Rect(self.rect.x, self.rect.y, tile + self.buffer, tile + self.buffer)

        self.type = 'wall'
        self.enemy_type = 'wall'

        self.rect.topleft = position

        self.color = (0, 0, 0)


    def update(self, player):
        hit = pygame.Rect.colliderect(self.rect, player.attack_rect)

        if hit:
            self.rect.x = 10000
