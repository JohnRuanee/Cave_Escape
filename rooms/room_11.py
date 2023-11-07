import pygame

import entities.bat
import walls.wall
from walls import button, door, stationary_shooter
from functions import functions

tile = 16

class Room():
    def __init__(self, door_num, screen, player):
        self.door = door_num

        self.screen = screen

        if self.door == 0:
            self.player_spawn = [(5.4 * tile, 2.4 * tile)]
        elif self.door == 1:
            self.player_spawn = [(5.4 * tile, 12.6 * tile)]
        elif self.door == 3:
            self.player_spawn = [(20.4 * tile, 7.4 * tile)]

        self.falling_walls = self.falling_walls_generate()

        self.doors = [door.Door((4 * tile, 1 * tile), 'down'), door.Door((4 * tile, 13.8 * tile), 'down'), door.Door((22 * tile, 6 * tile), 'left')]

        self.shooter = []
        self.buttons = []
        self.breakable_walls = []

        self.walls = functions.make_walls(self.doors)
        for i in range(5):
            self.walls.append(walls.wall.Wall(((10 + i) * tile, 14 * tile)))
            # self.walls.append(walls.wall.Wall(((22) * tile, (6 + i) * tile)))

        self.entities = []

        self.generate(player)

        self.button_bool = True

        self.room = 11

        self.adjacent_rooms = [1,12, 23]

    def update(self):
        key_event = pygame.key.get_pressed()
        self.draw_hitbox()

        for shooter in self.shooter:
            shooter.update(self.player, self.walls, not self.buttons[0].is_on)

        for button in self.buttons:
            button.update(self.player)

        for entity in self.entities:
            entity.update(self.player, self.walls, self.doors)

        self.player.update(key_event, self.screen, self.entities, self.walls, self.falling_walls, self.doors)

        return self.room, self.door, self.screen


    def generate(self, player):
        self.player = player
        self.player.reset(self.player_spawn[0])



    def falling_walls_generate(self):
        falling_walls = []

        for x in range(4):
            for y in range(12):
                falling_walls.append(walls.wall.Wall(((x + 10) * tile, (y + 2) * tile)))

        return falling_walls

    def draw_hitbox(self):
        self.screen.fill((255,255,255))

        pygame.draw.rect(self.screen, (0, 0, 255), self.player.rect)

        for wall in self.walls:
            pygame.draw.rect(self.screen, (0, 0, 0), wall.rect)

        for wall in self.falling_walls:
            pygame.draw.rect(self.screen, (0, 50, 150), wall.rect)

        for button in self.buttons:
            pygame.draw.rect(self.screen, (255, 0, 0), button.rect)

        for entity in self.entities:
            pygame.draw.rect(self.screen, (50, 50, 50), entity.rect)



    def room_door(self):

        return self.room, self.door

    def change_room(self, door):
        self.room = self.adjacent_rooms[door]
        self.door = 0

        match self.room:
            case 1:
                self.door = 3
            case 12:
                self.door = 0
            case 23:
                self.door = 1



    def reset(self):
        self.generate(self.player)
