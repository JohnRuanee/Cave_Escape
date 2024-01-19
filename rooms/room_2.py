import pygame
from walls import button, door, stationary_shooter
from functions import functions

tile = 16

class Room_2():
    def __init__(self, door_num, screen, player):
        self.door = door_num

        self.buttons = []
        self.entities = []
        self.shooter = []

        self.screen = screen

        if self.door == 0:
            self.player_spawn = [(2.4 * tile, 6 * tile)]
        else:
            self.player_spawn = [(20.6 * tile, 6 * tile)]

        self.falling_walls = self.falling_walls_generate()

        self.doors = [door.Door((1.1 * tile, 6 * tile), 'right'), door.Door((22 * tile, 6 * tile), 'left')]

        self.shooter = []
        self.buttons = []
        self.breakable_walls = []

        self.walls = functions.make_walls(self.doors)

        self.generate(player)

        self.button_bool = True

        self.room = 2

        self.adjacent_rooms = [1,3]

    def update(self):
        key_event = pygame.key.get_pressed()

        self.draw()

        for shooter in self.shooter:
            shooter.update(self.player, self.walls, not self.buttons[0].is_on)

        for button in self.buttons:
            button.update(self.player)

        self.player.update(key_event, self.screen, [], self.walls, self.falling_walls, self.doors)

        return self.room, self.door, self.screen


    def generate(self, player):
        self.player = player
        self.player.reset(self.player_spawn[0])

        self.button_bool = True

        self.shooter.append(stationary_shooter.Stationary_Shooter
                          ((6 * tile, 2 * tile), 'down', 6, self.screen))
        self.shooter.append(stationary_shooter.Stationary_Shooter
                          ((16 * tile, 2 * tile), 'down', 14, self.screen))
        self.shooter.append(stationary_shooter.Stationary_Shooter
                            ((16 * tile, 13 * tile), 'up', 14, self.screen))

        for shooter in self.shooter:
            self.walls.append(shooter)

        self.buttons.append(button.Button((10 * tile, 7.5 * tile), True, self.screen))

    def falling_walls_generate(self):
        falling_walls = []

        return falling_walls

    def draw(self):
        image = pygame.image.load('map/images/Room_2.png')
        pygame.Surface.blit(self.screen, image, (0, 0))

    def room_door(self):

        return self.room, self.door

    def change_room(self, door):
        self.room = self.adjacent_rooms[door]
        self.door = 0

        match self.room:
            case 1:
                self.door = 1
            case 3:
                self.door = 0

    def reset(self):
        self.generate(self.player)
