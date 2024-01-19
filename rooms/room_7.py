import pygame
from functions import functions
from walls import door, wall

tile = 16

class Room():
    def __init__(self, door_num, screen, player):
        self.door = door_num

        self.buttons = []
        self.entities = []
        self.shooter = []

        self.falling_walls = []
        self.breakable_walls = []

        if self.door == 0:
            self.player_spawn = [(2.4 * tile, 7.4 * tile)]
        else:
            self.player_spawn = [(17.4 * tile, 12.4 * tile)]

        self.generate(player)

        self.walls = functions.make_walls(self.doors)
        for i in range(5):
            self.walls.append(wall.Wall(((22) * tile, (6 + i) * tile)))

        self.room = 7

        self.screen = screen

        self.adjacent_rooms = [6,8]

    def update(self):
        key_event = pygame.key.get_pressed()
        self.draw()

        self.player.update(key_event, self.screen, [], self.walls, [], self.doors)

        self.give_sword()

        if not self.player.can_attack:
            image = pygame.image.load('entities/sprites/sword7.png')
            pygame.Surface.blit(self.screen, pygame.transform.scale(image,(1*tile, 2*tile)), (120, 110))

        return self.room, self.door, self.screen

    def draw(self):
        image = pygame.image.load('map/images/Room_' + str(self.room) + '.png')
        pygame.Surface.blit(self.screen, image, (0, 0))

    def generate(self, player):
        self.player = player
        self.player.reset(self.player_spawn[0])

        self.doors = [door.Door((1.1 * tile, 6 * tile), 'right'), door.Door((16 * tile, 13.8 * tile), 'down')]

        self.sword_box = pygame.Rect((8 * tile, 5 * tile, 4 * tile, 6 * tile))

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