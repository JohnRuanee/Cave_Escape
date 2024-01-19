import pygame
from functions import functions
from walls import door

tile = 16

class Room_0():
    def __init__(self, door_num, screen, player):
        self.door = door_num

        if door == 0:
            self.player_spawn = [(20.4 * tile, 6 * tile)]
        else:
            self.player_spawn = [(4 * tile, 6 * tile)]

        self.generate(player)

        self.walls = functions.make_walls(self.doors)
        self.room = 0

        self.buttons = []
        self.entities = []
        self.shooter = []
        self.falling_walls = []
        self.breakable_walls = []

        self.screen = screen

        self.adjacent_rooms = [1]

    def update(self):
        key_event = pygame.key.get_pressed()
        self.draw()

        self.player.update(key_event, self.screen, [], self.walls, [], self.doors)

        return self.room, self.door, self.screen


    def generate(self, player):
        self.player = player
        self.player.reset(self.player_spawn[0])

        self.doors = [door.Door((22 * tile, 6 * tile), 'left')]

    def draw(self):
        image = pygame.image.load('map/images/Room_0.png')
        pygame.Surface.blit(self.screen, image, (0,0))

    def room_door(self):

        return self.room, self.door

    def change_room(self, door):

        self.room = 1
        self.door = door