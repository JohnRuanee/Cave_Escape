import pygame
from functions import functions
from walls import door

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
            self.player_spawn = [(20.6 * tile, 7.4 * tile)]

        self.generate(player)

        self.walls = functions.make_walls(self.doors)
        self.room = 6

        self.screen = screen

        self.adjacent_rooms = [5,7]

    def update(self):
        key_event = pygame.key.get_pressed()
        self.draw()

        self.player.update(key_event, self.screen, [], self.walls, [], self.doors)

        return self.room, self.door, self.screen

    def draw(self):
        image = pygame.image.load('map/images/Room_' + str(self.room) + '.png')
        pygame.Surface.blit(self.screen, image, (0, 0))

    def generate(self, player):
        self.player = player
        self.player.reset(self.player_spawn[0])

        self.doors = [door.Door((1.1 * tile, 6 * tile), 'right'), door.Door((22 * tile, 6 * tile), 'left')]

    def room_door(self):

        return self.room, self.door

    def change_room(self, door):
        self.room = self.adjacent_rooms[door]
        self.door = 0

        match self.room:
            case 5:
                self.door = 1
            case 7:
                self.door = 0