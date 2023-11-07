import pygame
from functions import functions
from walls import door

tile = 16

class Room_99():
    def __init__(self, door_num, screen, player):
        self.door = door_num

        self.player = player

        self.player_spawn = [(4 * tile, 6 * tile)]


        self.generate(player)

        self.walls = functions.make_walls(self.doors)
        self.room = 99

        self.screen = screen

        self.adjacent_rooms = [0]

    def update(self):
        key_event = pygame.key.get_pressed()
        self.draw_hitbox()

        self.player.update(key_event, self.screen, [], self.walls, [], self.doors)

        return self.room, self.door, self.screen


    def generate(self, player):
        self.player = player
        self.player.reset(self.player_spawn[0])

        self.doors = [door.Door((22 * tile, 6 * tile), 'left')]

    def draw_hitbox(self):
        self.screen.fill((255,255,255))

        pygame.draw.rect(self.screen, (0, 0, 255), self.player.rect)
        pygame.draw.rect(self.screen, (255, 0, 255), self.doors[0])

        for wall in self.walls:
            pygame.draw.rect(self.screen, (0, 0, 0), wall.rect)

    def room_door(self):

        return self.room, self.door

    def change_room(self, door):

        self.room = self.adjacent_rooms[door]
        self.door = door