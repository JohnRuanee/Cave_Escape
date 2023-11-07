import pygame
from functions import functions
from walls import door, wall

tile = 16

class Room():
    def __init__(self, door_num, screen, player):
        self.door = door_num

        if self.door == 0:
            self.player_spawn = [(2.4 * tile, 7.4 * tile)]
        else:
            self.player_spawn = [(20.6 * tile, 7.4 * tile)]

        self.generate(player)

        self.walls = functions.make_walls(self.doors)
        for i in range(5):
            self.walls.append(wall.Wall(((22) * tile, (6 + i) * tile)))

        self.room = 7

        self.screen = screen

        self.adjacent_rooms = [6,8]

    def update(self):
        key_event = pygame.key.get_pressed()
        self.draw_hitbox()

        self.player.update(key_event, self.screen, [], self.walls, [], self.doors)

        self.give_sword()

        return self.room, self.door, self.screen


    def generate(self, player):
        self.player = player
        self.player.reset(self.player_spawn[0])

        self.doors = [door.Door((1.1 * tile, 6 * tile), 'right'), door.Door((16 * tile, 13.8 * tile), 'down')]

        self.sword_box = pygame.Rect((8 * tile, 5 * tile, 4 * tile, 6 * tile))

    def draw_hitbox(self):
        self.screen.fill((255,255,255))

        pygame.draw.rect(self.screen, (0, 0, 255), self.player.rect)

        for wall in self.walls:
            pygame.draw.rect(self.screen, (0, 0, 0), wall.rect)

        pygame.draw.rect(self.screen,(255, 255, 0 ), self.sword_box)

    def give_sword(self):
        give_sword_hit = pygame.Rect.colliderect(self.sword_box, self.player.rect)

        if give_sword_hit:
            self.player.can_attack = True

    def room_door(self):

        return self.room, self.door

    def change_room(self, door):
        self.room = self.adjacent_rooms[door]
        self.door = 0

        match self.room:
            case 6:
                self.door = 1
            case 8:
                self.door = 0