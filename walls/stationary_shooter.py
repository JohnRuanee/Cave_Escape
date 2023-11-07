import pygame
import random

tile = 16

class Stationary_Shooter(pygame.sprite.Sprite):
    def __init__(self, position, direction, rof, screen):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, tile, tile)
        self.color = (50, 50, 50)
        self.facing = direction

        self.screen = screen

        self.attack_rect = pygame.Rect(0,0,0,0)
        self.attack = False
        self.attack_timer = 0
        self.attack_speed = rof

        self.bullet_rect = pygame.Rect(0,0,0,0)
        self.bullet_size = 4
        self.bullet_speed = 4
        self.bullet_direction = 'left'

        self.health = 2
        self.curr_hit = False

        self.type = 'wall'
        self.enemy_type = 'wall'

        self.rect.topleft = position




    def update(self, player, walls, attack_on):
        if attack_on:
            self.call_attack()
            self.attack_update(player, walls)
        else:
            self.attack_timer = 0
            self.bullet_rect.x = 10000



    def attack_update(self, player, walls):
        if self.attack_timer > 0:
            match self.bullet_direction:
                case 'left':
                    self.bullet_rect.x -= self.bullet_speed
                case 'right':
                    self.bullet_rect.x += self.bullet_speed
                case 'up':
                    self.bullet_rect.y -= self.bullet_speed
                case 'down':
                    self.bullet_rect.y += self.bullet_speed
            self.attack_timer -= self.attack_speed
        else:
            self.attack = False

        pygame.draw.rect(self.screen, (255, 0, 0), self.bullet_rect)

        bullet_hit = pygame.Rect.colliderect(self.bullet_rect, player.rect)
        if bullet_hit:
            player.damage(walls)
            self.attack_timer = 30
            self.bullet_rect.x = 10000

    def attack_rect(self):
        return self.attack_rect

    def collision_rect(self):
        return self.rect

    def call_attack(self):
        if not self.attack:
            self.attack_timer = tile * 16
            self.attack = True

            match self.facing:
                case 'left':
                    self.bullet_rect = pygame.Rect(self.rect.x - self.bullet_size, self.rect.y + (tile / 2) -
                                                   (self.bullet_size / 2), self.bullet_size, self.bullet_size)
                    self.bullet_direction = 'left'
                case 'right':
                    self.bullet_rect = pygame.Rect(self.rect.x + tile + self.bullet_size, self.rect.y + (tile / 2) -
                                                   (self.bullet_size / 2), self.bullet_size, self.bullet_size)
                    self.bullet_direction = 'right'
                case 'up':
                    self.bullet_rect = pygame.Rect(self.rect.x + (tile / 2) - (self.bullet_size / 2), self.rect.y -
                                                   self.bullet_size, self.bullet_size, self.bullet_size)
                    self.bullet_direction = 'up'
                case 'down':
                    self.bullet_rect = pygame.Rect(self.rect.x + (tile / 2) - (self.bullet_size / 2), self.rect.y +
                                                   tile + self.bullet_size, self.bullet_size, self.bullet_size)
                    self.bullet_direction = 'down'





