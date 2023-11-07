import pygame
import random

tile = 16

class Bat(pygame.sprite.Sprite):
    def __init__(self, position, screen):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, tile, tile)
        self.color = (50, 50, 50)
        self.facing = 'right'

        self.screen = screen

        self.attack_rect = pygame.Rect(0,0,0,0)
        self.attack = False
        self.attack_timer = 0
        self.attack_speed = 4

        self.bullet_rect = pygame.Rect(0,0,0,0)
        self.bullet_size = 4
        self.bullet_speed = 4
        self.bullet_direction = 'left'

        self.health = 2
        self.curr_hit = False

        self.moving_rect = pygame.Rect(0, 0, 0 * tile, 0 * tile)
        self.move_timer = 30
        self.moving_timer = 0
        self.hit_timer = 0
        self.knock_back_speed = 8

        self.collision_rect = pygame.Rect(0, 0, 0 * tile, 0 * tile)
        self.collision_buffer = 2

        self.rect.topleft = position
        pygame.sprite.Group()

    def update(self, player_group, walls, enemy_walls):
        self.moving_update(walls, enemy_walls)
        self.attack_update()
        self.collision_update(player_group, walls)

    def moving_update(self, walls, enemy_walls):
        if self.move_timer <= 0 and self.moving_timer <= 0:
            num = random.randint(1, 3)
            if num == 3:
                self.moving_timer = 48
                num = random.randint(1, 4)

                match num:
                    case 1:
                        self.facing = 'left'
                    case 2:
                        self.facing = 'right'
                    case 3:
                        self.facing = 'up'
                    case 4:
                        self.facing = 'down'

            else:
                self.move_timer = 30
        else:
            self.move_timer -= 1

        match self.facing:
            case 'left':
                self.collision_rect = pygame.Rect(self.rect.x - self.collision_buffer, self.rect.y,
                                                  self.collision_buffer, tile)
            case 'right':
                self.collision_rect = pygame.Rect(self.rect.x + tile, self.rect.y,
                                                  self.collision_buffer, tile)
            case 'up':
                self.collision_rect = pygame.Rect(self.rect.x, self.rect.y - self.collision_buffer,
                                                  tile, self.collision_buffer)
            case 'down':
                self.collision_rect = pygame.Rect(self.rect.x, self.rect.y + tile,
                                                  tile, self.collision_buffer)

        if self.moving_timer > 0:
            match self.facing:
                case 'left':
                    if not self.collision_check(walls, enemy_walls):
                        self.rect.x -= 1
                case 'right':
                    if not self.collision_check(walls, enemy_walls):
                        self.rect.x += 1
                case 'up':
                    if not self.collision_check(walls, enemy_walls):
                        self.rect.y -= 1
                case 'down':
                    if not self.collision_check(walls, enemy_walls):
                        self.rect.y += 1

            self.moving_timer -= 1

    def attack_update(self):
        distance = 16
        match self.facing:
            case 'left':
                self.attack_rect = pygame.Rect(self.rect.x - distance * tile, self.rect.y, distance * tile, tile)
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(self.rect.x - 1, self.attack_rect.y, 1, tile))
            case 'right':
                self.attack_rect = pygame.Rect(self.rect.x + 1 * tile, self.rect.y, distance * tile, tile)
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(self.attack_rect.x, self.attack_rect.y, 1, tile))
            case 'up':
                self.attack_rect = pygame.Rect(self.rect.x, self.rect.y - distance * tile, tile, distance * tile)
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(self.attack_rect.x, self.rect.y - 1, tile, 1))
            case 'down':
                self.attack_rect = pygame.Rect(self.rect.x, self.rect.y + 1 * tile, tile, distance * tile)
                pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(self.attack_rect.x, self.attack_rect.y, tile, 1))



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



    def collision_update(self, player, walls):
        attack_box_hit = pygame.Rect.colliderect(self.attack_rect, player.rect)
        if attack_box_hit:
            self.call_attack()

        bullet_hit = pygame.Rect.colliderect(self.bullet_rect, player.rect)
        if bullet_hit:
            player.damage(walls)
            self.attack_timer = 30
            self.bullet_rect.x = 10000

        hit = pygame.Rect.colliderect(self.rect, player.attack_rect)
        if hit and not self.curr_hit:
            self.hit()
            self.curr_hit = True

        if not hit:
            self.curr_hit = False

        if self.hit_timer > 0:
            match player.facing:
                case 'left':
                    self.rect.x -= self.knock_back_speed
                case 'right':
                    self.rect.x += self.knock_back_speed
                case 'up':
                    self.rect.y -= self.knock_back_speed
                case 'down':
                    self.rect.y += self.knock_back_speed

            self.hit_timer -= self.knock_back_speed


    def hit(self):
        self.health -= 1
        self.hit_timer = 2 * tile

        if self.health <= 0:
            self.rect.topleft = (10000, 10000)

    def collision_check(self, walls, enemy_walls):
        match self.facing:
            case 'left':
                for wall in walls:
                    if pygame.Rect.colliderect(self.collision_rect, wall.rect):
                        return True
                for wall in enemy_walls:
                    if pygame.Rect.colliderect(self.collision_rect, wall.rect):
                        return True
            case 'right':
                for wall in walls:
                    if pygame.Rect.colliderect(self.collision_rect, wall.rect):
                        return True
                for wall in enemy_walls:
                    if pygame.Rect.colliderect(self.collision_rect, wall.rect):
                        return True
            case 'up':
                for wall in walls:
                    if pygame.Rect.colliderect(self.collision_rect, wall.rect):
                        return True
                for wall in enemy_walls:
                    if pygame.Rect.colliderect(self.collision_rect, wall.rect):
                        return True
            case 'down':
                for wall in walls:
                    if pygame.Rect.colliderect(self.collision_rect, wall.rect):
                        return True
                for wall in enemy_walls:
                    if pygame.Rect.colliderect(self.collision_rect, wall.rect):
                        return True