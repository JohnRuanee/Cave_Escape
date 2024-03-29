import pygame
import random

tile = 16

class Bug(pygame.sprite.Sprite):
    def __init__(self, position, screen):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, tile, tile)
        self.color = (255, 0, 255)
        self.facing = 'right'

        self.screen = screen

        self.attack_rect = pygame.Rect(0,0,0,0)
        self.attack = False
        self.attack_timer = 0

        self.health = 2
        self.curr_hit = False

        self.collision_rect = pygame.Rect(0, 0, 0 * tile, 0 * tile)
        self.collision_buffer = 2

        self.move_timer = 30
        self.moving_timer = 0


        self.hit_timer = 0
        self.knock_back_speed = 8

        self.rect.topleft = position
        pygame.sprite.Group()

        self.progressed = False

        # load image
        self.sheet = pygame.image.load("entities/sprites/bug32.png")

        # defines area of a single sprite of an image
        self.sheet.set_clip(pygame.Rect(0, 0, 2 * tile, 2 * tile))

        # loads spritesheet images
        self.image = self.sheet.subsurface(self.sheet.get_clip())

        self.frame = 0

        self.down_states = {0: (0 * tile, 0 * tile, 2 * tile, 2 * tile),
                            1: (2 * tile, 0 * tile, 2 * tile, 2 * tile),
                            2: (4 * tile, 0 * tile, 2 * tile, 2 * tile),
                            3: (6 * tile, 0 * tile, 2 * tile, 2 * tile)}

        self.right_states = {0: (0 * tile, 2 * tile, 2 * tile, 2 * tile),
                             1: (2 * tile, 2 * tile, 2 * tile, 2 * tile),
                             2: (4 * tile, 2 * tile, 2 * tile, 2 * tile),
                             3: (6 * tile, 2 * tile, 2 * tile, 2 * tile)}

        self.up_states = {0: (0 * tile, 4 * tile, 2 * tile, 2 * tile),
                          1: (2 * tile, 4 * tile, 2 * tile, 2 * tile),
                          2: (4 * tile, 4 * tile, 2 * tile, 2 * tile),
                          3: (6 * tile, 4 * tile, 2 * tile, 2 * tile)}

        self.left_states = {0: (0 * tile, 6 * tile, 2 * tile, 2 * tile),
                            1: (2 * tile, 6 * tile, 2 * tile, 2 * tile),
                            2: (4 * tile, 6 * tile, 2 * tile, 2 * tile),
                            3: (6 * tile, 6 * tile, 2 * tile, 2 * tile)}


    def update(self, player_group, walls, enemy_walls):
        self.moving_update(walls, enemy_walls)
        self.attack_update(walls, enemy_walls)
        self.collision_update(player_group, walls, enemy_walls)
        self.animation_update(self.facing)

    def get_frame(self, frame_set):
        # looping the sprite sequences.
        if not self.progressed:
            self.frame += 1
            self.progressed = True
        else:
            self.progressed = False

        # if loop index is higher that the size of the frame return to the first frame
        if self.frame > (len(frame_set) - 1):
            self.frame = 1
        # print(frame_set[self.frame])
        return frame_set[self.frame]

    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    def animation_update(self, direction):
        if direction == 'left':
            self.clip(self.left_states)

        if direction == 'right':
            self.clip(self.right_states)

        if direction == 'up':
            self.clip(self.up_states)

        if direction == 'down':
            self.clip(self.down_states)


        self.image = self.sheet.subsurface(self.sheet.get_clip())

        self.screen.blit(self.image, (self.rect.x - 8, self.rect.y - 8))

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

    def attack_update(self, walls, enemy_walls):
        match self.facing:
            case 'left':
                self.attack_rect = pygame.Rect(self.rect.x - 3 * tile, self.rect.y, 3 * tile, tile)
                # pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(self.rect.x - 1, self.attack_rect.y, 1, tile))
            case 'right':
                self.attack_rect = pygame.Rect(self.rect.x + 1 * tile, self.rect.y, 3 * tile, tile)
                # pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(self.attack_rect.x, self.attack_rect.y, 1, tile))
            case 'up':
                self.attack_rect = pygame.Rect(self.rect.x, self.rect.y - 3 * tile, tile, 3 * tile)
                # pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(self.attack_rect.x, self.rect.y - 1, tile, 1))
            case 'down':
                self.attack_rect = pygame.Rect(self.rect.x, self.rect.y + 1 * tile, tile, 3 * tile)
                # pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(self.attack_rect.x, self.attack_rect.y, tile, 1))

        # pygame.draw.rect(self.screen, (0, 255, 0), self.attack_rect)

        if self.attack_timer > 0:
            speed = 4
            match self.facing:
                case 'left':
                    if not self.collision_check(walls, enemy_walls):
                        self.rect.x -= speed
                case 'right':
                    if not self.collision_check(walls, enemy_walls):
                        self.rect.x += speed
                case 'up':
                    if not self.collision_check(walls, enemy_walls):
                        self.rect.y -= speed
                case 'down':
                    if not self.collision_check(walls, enemy_walls):
                        self.rect.y += speed
            self.attack_timer -= speed
        else:
            self.attack = False

    def attack_rect(self):
        return self.attack_rect

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

    def call_attack(self):
        if not self.attack:
            self.attack_timer = tile * 2
            self.attack = True

    def collision_update(self, player, walls, enemy_walls):
        attack_box_hit = pygame.Rect.colliderect(self.attack_rect, player.rect)
        if attack_box_hit:
            self.call_attack()

        hit = pygame.Rect.colliderect(self.rect, player.attack_rect)
        if hit and not self.curr_hit:
            self.hit()
            self.curr_hit = True

        if not hit:
            self.curr_hit = False

        if self.hit_timer > 0:
            match player.facing:
                case 'left':
                    if not self.collision_check(walls, enemy_walls):
                        self.rect.x -= self.knock_back_speed
                case 'right':
                    if not self.collision_check(walls, enemy_walls):
                        self.rect.x += self.knock_back_speed
                case 'up':
                    if not self.collision_check(walls, enemy_walls):
                        self.rect.y -= self.knock_back_speed
                case 'down':
                    if not self.collision_check(walls, enemy_walls):
                        self.rect.y += self.knock_back_speed

            self.hit_timer -= self.knock_back_speed

    def hit(self):
        self.health -= 1
        self.hit_timer = 2 * tile

        if self.health <= 0:
            self.rect.topleft = (10000, 10000)





