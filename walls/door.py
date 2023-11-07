import pygame

tile = 16

class Door(pygame.sprite.Sprite):
    def __init__(self, position, facing):
        pygame.sprite.Sprite.__init__(self)

        if facing == 'left' or facing == 'right':
            self.rect = pygame.Rect(0, 0, 1.3*tile, 5*tile)
        else:
            self.rect = pygame.Rect(0, 0, 5 * tile, 1.3 * tile)

        self.facing = facing

        self.buffer = 2
        self.buffer_rect = pygame.Rect(self.rect.x, self.rect.y, tile + self.buffer, tile + self.buffer)

        self.type = 'wall'
        self.enemy_type = 'wall'

        self.rect.topleft = position
        self.rect.x = self.rect.x - 1

        self.color = (0, 0, 0)
