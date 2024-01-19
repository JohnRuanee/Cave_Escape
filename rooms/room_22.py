import pygame

from entities import bug, bat
from walls import button, door, stationary_shooter, wall
from functions import functions

tile = 16

class Room():
    def __init__(self, door_num, screen, player):
        self.door = door_num

        self.screen = screen

        if self.door == 0:
            self.player_spawn = [(2.4 * tile, 3.4 * tile)]
        elif self.door == 1:
            self.player_spawn = [(2.4 * tile, 7.4 * tile)]
        elif self.door == 2:
            self.player_spawn = [(2.4 * tile, 11.4 * tile)]


        self.falling_walls = self.falling_walls_generate()

        self.doors = [door.Door((1 * tile, 2 * tile),  'left'),
                      door.Door((1 * tile, 6 * tile), 'left'),
                      door.Door((1 * tile, 10 * tile), 'left'),
                      door.Door((10 * tile, 1 * tile), 'up')]

        self.shooter = []
        self.buttons = []
        self.breakable_walls = []
        self.entity_walls = []

        self.walls = functions.make_walls(self.doors)
        for i in range(12):
            # self.walls.append(wall.Wall(((4 + i) * tile, 14 * tile)))
            self.walls.append(wall.Wall(((22) * tile, (2 + i) * tile)))

        self.entities = []

        self.generate(player)

        self.button_bool = True

        self.room = 22

        self.adjacent_rooms = [210,211,212, 28]

    def update(self):
        self.draw()

        key_event = pygame.key.get_pressed()

        for shooter in self.shooter:
            shooter.update(self.player, self.walls, not self.buttons[0].is_on)

        for button in self.buttons:
            button.update(self.player)

        for entity in self.entities:
            entity.update(self.player, self.entity_walls, self.doors)

        self.player.update(key_event, self.screen, self.entities, self.walls, self.falling_walls, self.doors)

        return self.room, self.door, self.screen

    def draw(self):
        image = pygame.image.load('map/images/Room_' + str(self.room) + '.png')
        pygame.Surface.blit(self.screen, image, (0, 0))

    def generate(self, player):
        self.player = player
        self.player.reset(self.player_spawn[0])

        for wall in self.walls:
            self.entity_walls.append(wall)
        for wall in self.falling_walls:
            self.entity_walls.append(wall)

    def falling_walls_generate(self):
        falling_walls = []

        return falling_walls

    def room_door(self):

        return self.room, self.door

    def change_room(self, door):
        self.room = self.adjacent_rooms[door]
        self.door = 0

        match self.room:
            case 210:
                self.door = 1
                self.room = 21
            case 211:
                self.door = 2
                self.room = 21
            case 212:
                self.door = 3
                self.room = 21
            case 28:
                self.room = 28

    def reset(self):
        del self.entities
        self.entities = []

        del self.shooter
        self.shooter = []

        self.generate(self.player)

        self.player.health = 3
