import pygame

import walls.wall
from walls import button, door, stationary_shooter, breakable_wall
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
            self.player_spawn = [(2.4 * tile, 7.5 * tile)]
        elif self.door == 1:
            self.player_spawn = [(17.5 * tile, 2.4 * tile)]
        else:
            self.player_spawn = [(20.6 * tile, 7.5 * tile)]

        self.falling_walls = self.falling_walls_generate()

        self.doors = [door.Door((1.1 * tile, 6 * tile), 'right'), door.Door((16 * tile, 1 * tile), 'down'), door.Door((22 * tile, 6 * tile), 'left')]

        self.shooter = []
        self.buttons = []
        self.breakable_walls = []

        self.walls = functions.make_walls(self.doors)
        for i in range(5):
            self.walls.append(walls.wall.Wall(((16 + i) * tile, 14 * tile)))

        self.generate(player)

        self.button_bool = True

        self.room = 3

        self.adjacent_rooms = [2,4, 10]

    def update(self):
        key_event = pygame.key.get_pressed()
        self.draw()

        for shooter in self.shooter:
            shooter.update(self.player, self.walls, not self.buttons[0].is_on)

        for button in self.buttons:
            button.update(self.player)

        for wall in self.breakable_walls:
            wall.update(self.player)

        self.player.update(key_event, self.screen, [], self.walls, self.falling_walls, self.doors)

        return self.room, self.door, self.screen


    def generate(self, player):
        self.player = player
        self.player.reset(self.player_spawn[0])

        for i in range(6):
            self.breakable_walls.append(breakable_wall.Breakable_Wall((19 * tile, (5 + i) * tile)))

        for i in range(2):
            self.breakable_walls.append(breakable_wall.Breakable_Wall(((20 + i) * tile, (5) * tile)))
        for i in range(2):
            self.breakable_walls.append(breakable_wall.Breakable_Wall(((20 + i) * tile, (10) * tile)))

        for wall in self.breakable_walls:
            self.walls.append(wall)

    def falling_walls_generate(self):
        falling_walls = []

        return falling_walls

    def draw(self):
        image = pygame.image.load('map/images/Room_' + str(self.room) + '.png')
        pygame.Surface.blit(self.screen, image, (0, 0))



    def room_door(self):

        return self.room, self.door

    def change_room(self, door):
        self.room = self.adjacent_rooms[door]
        self.door = 0

        match self.room:
            case 2:
                self.door = 1
            case 4:
                self.door = 0
            case 10:
                self.door = 1


    def reset(self):
        self.generate(self.player)
