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
        self.moving = False

        self.rect.topleft = position

        self.buffer_rect_left = pygame.Rect(0, 0, 2, tile)
        self.buffer_rect_right = pygame.Rect(0, 0, 2, tile)
        self.buffer_rect_up = pygame.Rect(0, 0, tile, 2)
        self.buffer_rect_down = pygame.Rect(0, 0, tile, 2)
        self.buffer = 2

        self.falling_rect = falling_rect.Falling_Rect(self.rect)

        # load image
        self.slash_sheet = pygame.image.load("entities/sprites/slash.png")

        # defines area of a single sprite of an image
        self.slash_sheet.set_clip(pygame.Rect(0, 0, 38, 38))

        # loads spritesheet images
        self.slash_image = self.slash_sheet.subsurface(self.slash_sheet.get_clip())

        self.heart_full = pygame.image.load("entities/sprites/Red 16.png")
        self.heart_empty = pygame.image.load("entities/sprites/16.png")

        self.frame_slash = 0
        self.frame = 0

        self.slash_states = {0: (35, 0 * tile, 35, 2 * tile),
                             3: (70, 0 * tile, 35, 2 * tile),
                             1: (0 * tile, 2 * tile, 35, 2 * tile),
                             2: (35, 2 * tile, 35, 2 * tile)}

        self.progressed = False

        # load image
        self.sheet = pygame.image.load("entities/sprites/player_sprite.png")

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



    def update(self, key, screen, entities, walls, falling_walls, doors):
        self.screen = screen
        self.movement_update(key, walls)
        if self.can_attack:
            self.attack_update(key, screen)
        self.collision_update(entities, walls, falling_walls, doors)
        self.buffer_update()
        self.animation_update(self.facing)

        if self.health == 3:
            screen.blit(self.heart_full, (0,0))
            screen.blit(self.heart_full, (0, 1 * tile))
            screen.blit(self.heart_full, (0, 2 * tile))
        elif self.health == 2:
            screen.blit(self.heart_full, (0,0))
            screen.blit(self.heart_full, (0, 1 * tile))
            screen.blit(self.heart_empty, (0, 2 * tile))
        elif self.health == 1:
            screen.blit(self.heart_full, (0, 0))
            screen.blit(self.heart_empty, (0, 1 * tile))
            screen.blit(self.heart_empty, (0, 2 * tile))
        else:
            screen.blit(self.heart_empty, (0, 0))
            screen.blit(self.heart_empty, (0, 1 * tile))
            screen.blit(self.heart_empty, (0, 2 * tile))

    def get_frame_slash(self, frame_set):
        # looping the sprite sequences.
        if not self.progressed:
            self.frame_slash += 1
            self.progressed = True
        else:
            self.progressed = False
        # self.frame += 1

        # if loop index is higher that the size of the frame return to the first frame
        if self.frame_slash > 3:
            self.frame_slash = 0
        # print(frame_set[self.frame])
        return frame_set[self.frame_slash]

    def clip_slash(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.slash_sheet.set_clip(pygame.Rect(self.get_frame_slash(clipped_rect)))
        else:
            self.slash_sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

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

        if not self.moving:
            self.frame = 0

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

    def animation_update_slash(self, direction):
        if direction == 'left':
            self.clip_slash(self.slash_states)
            self.slash_image = self.slash_sheet.subsurface(self.slash_sheet.get_clip())
            self.screen.blit(pygame.transform.rotate(self.slash_image, 90), (self.attack_rect.x - 0, self.attack_rect.y - 8))


        if direction == 'right':
            self.clip_slash(self.slash_states)
            self.slash_image = self.slash_sheet.subsurface(self.slash_sheet.get_clip())
            self.screen.blit(pygame.transform.rotate(self.slash_image, 270), (self.attack_rect.x - 16, self.attack_rect.y - 8))

        if direction == 'up':
            self.clip_slash(self.slash_states)
            self.slash_image = self.slash_sheet.subsurface(self.slash_sheet.get_clip())
            self.screen.blit(pygame.transform.rotate(self.slash_image, 0), (self.attack_rect.x - 8, self.attack_rect.y - 0))

        if direction == 'down':
            self.clip_slash(self.slash_states)
            self.slash_image = self.slash_sheet.subsurface(self.slash_sheet.get_clip())
            self.screen.blit(pygame.transform.rotate(self.slash_image, 180), (self.attack_rect.x - 8, self.attack_rect.y - 16))

        # self.clip(self.slash_states)



    def movement_update(self, key, walls):
        move = False
        if self.movable:
            if (key[pygame.K_LEFT]):
                self.facing = 'left'
                # self.animation_update(self.facing)
                move = True

                if not self.buffer_collision(walls):
                    self.rect.x -= 5

            if (key[pygame.K_RIGHT]):
                self.facing = 'right'
                # self.animation_update(self.facing)
                move = True

                if not self.buffer_collision(walls):
                    self.rect.x += 5

            if (key[pygame.K_UP]):
                self.facing = 'up'
                # self.animation_update(self.facing)
                move = True

                if not self.buffer_collision(walls):
                    self.rect.y -= 5

            if (key[pygame.K_DOWN]):
                self.facing = 'down'
                # self.animation_update(self.facing)
                move = True

                if not self.buffer_collision(walls):
                    self.rect.y += 5

            if move:
                self.moving = True
            else:
                self.moving = False



    def attack_update(self, key, screen):
        if (key[pygame.K_x] and self.attack == False):
            self.attack = True
            self.attack_timer = 6

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

            # pygame.draw.rect(screen, (255, 0, 0), self.attack_rect)
            self.animation_update_slash(self.facing)

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

