import pygame
from functions import falling_rect

tile = 16

class Player(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.room = None
        self.rect = pygame.Rect(0, 0, 16, 16)
        self.color = (0, 0, 255)
        self.facing = 'right'

        self.attack_rect = pygame.Rect(-20, -20, 16, 16)
        self.attack = False
        self.attack_timer = 0
        self.can_attack = False

        self.health = 3
        self.hit = False
        self.hit_timer = 0
        self.movable = True

        self.rect.topleft = position

        self.buffer_rect_left = pygame.Rect(0, 0, 2, tile)
        self.buffer_rect_right = pygame.Rect(0, 0, 2, tile)
        self.buffer_rect_up = pygame.Rect(0, 0, tile, 2)
        self.buffer_rect_down = pygame.Rect(0, 0, tile, 2)
        self.buffer = 2

        self.falling_rect = falling_rect.Falling_Rect(self.rect)



    def update(self, key, screen, entities, walls, falling_walls, doors):
        self.movement_update(key, walls)
        if self.can_attack:
            self.attack_update(key, screen)
        self.collision_update(entities, walls, falling_walls, doors)
        self.buffer_update()



    def movement_update(self, key, walls):
        if self.movable:
            if (key[pygame.K_LEFT]):
                self.facing = 'left'

                if not self.buffer_collision(walls):
                    self.rect.x -= 5

            if (key[pygame.K_RIGHT]):
                self.facing = 'right'

                if not self.buffer_collision(walls):
                    self.rect.x += 5

            if (key[pygame.K_UP]):
                self.facing = 'up'

                if not self.buffer_collision(walls):
                    self.rect.y -= 5

            if (key[pygame.K_DOWN]):
                self.facing = 'down'

                if not self.buffer_collision(walls):
                    self.rect.y += 5

    def attack_update(self, key, screen):
        if (key[pygame.K_x] and self.attack == False):
            self.attack = True
            self.attack_timer = 10

        if (self.attack == True):
            self.attack_timer -= 1

            match self.facing:
                case 'left':
                    self.attack_rect = pygame.Rect(self.rect.x - tile, self.rect.y, tile, tile)
                case 'right':
                    self.attack_rect = pygame.Rect(self.rect.x + tile, self.rect.y, tile, tile)
                case 'up':
                    self.attack_rect = pygame.Rect(self.rect.x, self.rect.y - tile, tile, tile)
                case 'down':
                    self.attack_rect = pygame.Rect(self.rect.x, self.rect.y + tile, tile, tile)

            pygame.draw.rect(screen, (255, 0, 0), self.attack_rect)

            if self.attack_timer <= 0:
                self.attack_rect.x = -20
                self.attack_rect.y = -20
                self.attack = False

    def collision_update(self, entities, walls, falling_walls, doors):
        hit = pygame.sprite.spritecollide(self, entities, False)

        if hit and not self.hit:
            self.health -= 1
            self.hit = True
            self.hit_timer = tile * 2

        self.hit_update(hit, walls)


        if self.falling_rect.check_collision(falling_walls):
            self.room.reset()

        on_door, door_num = self.falling_rect.check_collision_doors(doors)
        if on_door:
            self.change_room(door_num)




    def hit_update(self, hit, walls):
        if self.hit_timer > 0:
            match self.facing:
                case 'left':
                    if not self.buffer_collision_hit(walls):
                        self.rect.x += 4
                case 'right':
                    if not self.buffer_collision_hit(walls):
                        self.rect.x -= 4
                case 'up':
                    if not self.buffer_collision_hit(walls):
                        self.rect.y += 4
                case 'down':
                    if not self.buffer_collision_hit(walls):
                        self.rect.y -= 4

            self.hit_timer -= 4

        if self.hit_timer > tile:
            self.movable = False
        else:
            self.movable = True

        if not hit:
            self.hit = False

    def buffer_update(self):
        self.buffer_rect_left.x = self.rect.x - self.buffer
        self.buffer_rect_left.y = self.rect.y

        self.buffer_rect_right.x = self.rect.x + tile
        self.buffer_rect_right.y = self.rect.y

        self.buffer_rect_up.x = self.rect.x
        self.buffer_rect_up.y = self.rect.y - self.buffer

        self.buffer_rect_down.x = self.rect.x
        self.buffer_rect_down.y = self.rect.y + tile

    def damage(self, walls):
        if not self.hit:
            self.health -= 1
            self.hit = True
            self.hit_timer = tile * 2

        if self.health == 0:
            self.room.reset()

        self.hit_update(True, walls)

    def buffer_collision(self, walls):
        match self.facing:
            case 'left':
                for wall in walls:
                    if pygame.Rect.colliderect(self.buffer_rect_left, wall.rect):
                        return True
            case 'right':
                for wall in walls:
                    if pygame.Rect.colliderect(self.buffer_rect_right, wall.rect):
                        return True
            case 'up':
                for wall in walls:
                    if pygame.Rect.colliderect(self.buffer_rect_up, wall.rect):
                        return True
            case 'down':
                for wall in walls:
                    if pygame.Rect.colliderect(self.buffer_rect_down, wall.rect):
                        return True

    def buffer_collision_hit(self, walls):
        match self.facing:
            case 'left':
                for wall in walls:
                    if (pygame.Rect.colliderect(self.buffer_rect_left, wall.rect) or
                            pygame.Rect.colliderect(self.buffer_rect_right, wall.rect)):
                        return True
            case 'right':
                for wall in walls:
                    if (pygame.Rect.colliderect(self.buffer_rect_left, wall.rect) or
                            pygame.Rect.colliderect(self.buffer_rect_right, wall.rect)):
                        return True
            case 'up':
                for wall in walls:
                    if (pygame.Rect.colliderect(self.buffer_rect_up, wall.rect) or
                            pygame.Rect.colliderect(self.buffer_rect_down, wall.rect)):
                        return True
            case 'down':
                for wall in walls:
                    if (pygame.Rect.colliderect(self.buffer_rect_up, wall.rect) or
                            pygame.Rect.colliderect(self.buffer_rect_down, wall.rect)):
                        return True

    def reset(self, position):
        self.rect.topleft =  position

    def set_room(self, room):
        self.room = room

    def change_room(self, door_num):
        self.room.change_room(door_num)

