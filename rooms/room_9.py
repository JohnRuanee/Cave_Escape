import pygame

import entities.bat
import walls.wall
from walls import button, door, stationary_shooter
from functions import functions

tile = 16

class Room():
    def __init__(self, door_num, screen, player):
        self.door = door_num

        self.buttons = []
        self.entities = []
        self.shooter = []

        self.screen = screen

        if self.door == 0:
            self.player_spawn = [(11.4 * tile, 2.4 * tile)]
        else:
            self.player_spawn = [(12.4 * tile, 12.6 * tile)]

        self.falling_walls = self.falling_walls_generate()

        self.doors = [door.Door((10 * tile, 1 * tile), 'down'), door.Door((10 * tile, 13.5 * tile), 'down')]

        self.shooter = []
        self.buttons = []
        self.breakable_walls = []

        self.walls = functions.make_walls(self.doors)
        for i in range(5):
            self.walls.append(walls.wall.Wall(((14 + i) * tile, 14 * tile)))

        self.entities = []

        self.generate(player)

        self.button_bool = True

        self.room = 9

        self.adjacent_rooms = [8,10]

    def update(self):
        key_event = pygame.key.get_pressed()
        self.draw()

        for shooter in self.shooter:
            shooter.update(self.player, self.walls, not self.buttons[0].is_on)

        for button in self.buttons:
            button.update(self.player)

        for entity in self.entities:
            entity.update(self.player, self.walls, self.doors)

        self.player.update(key_event, self.screen, self.entities, self.walls, self.falling_walls, self.doors)

        return self.room, self.door, self.screen

    def draw(self):
        image = pygame.image.load('map/images/Room_' + str(self.room) + '.png')
        pygame.Surface.blit(self.screen, image, (0, 0))

    def generate(self, player):
        self.player = player
        self.player.reset(self.player_spawn[0])

        self.entities.append(entities.bat.Bat((8 * tile, 6 * tile), self.screen))
        self.entities.append(entities.bat.Bat((10 * tile, 8 * tile), self.screen))
        self.entities.append(entities.bat.Bat((12 * tile, 6 * tile), self.screen))
        self.entities.append(entities.bat.Bat((14 * tile, 8 * tile), self.screen))

    def falling_walls_generate(self):
        falling_walls = []



        return falling_walls

    def room_door(self):

        return self.room, self.door

    def change_room(self, door):
        self.room = self.adjacent_rooms[door]
        self.door = 0

        match self.room:
            case 8:
                self.door = 1
            case 10:
                self.door = 0



    def reset(self):
        self.generate(self.player)
