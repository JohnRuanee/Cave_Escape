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
            self.player_spawn = [(15.4 * tile, 11.4 * tile)]
        elif self.door == 1:
            self.player_spawn = [(21.4 * tile, 7.4 * tile)]
        else:
            self.player_spawn = [(2.4 * tile, 7.4 * tile)]

        self.falling_walls = self.falling_walls_generate()

        self.doors = [door.Door((14 * tile, 13.8 * tile), 'down'), door.Door((22 * tile, 6 * tile), 'left'), door.Door((1 * tile, 6 * tile), 'left'), door.Door((10 * tile, 1 * tile), 'down')]

        self.shooter = []
        self.buttons = []
        self.breakable_walls = []
        self.entity_walls = []

        self.walls = functions.make_walls(self.doors)
        for i in range(5):
            self.walls.append(wall.Wall(((10 + i) * tile, 1 * tile)))
            self.walls.append(wall.Wall(((9 + i) * tile, 14 * tile)))
            # self.walls.append(wall.Wall(((22) * tile, (6 + i) * tile)))

        self.entities = []

        self.generate(player)

        self.button_bool = True

        self.room = 17

        self.adjacent_rooms = [16,18, 23]

    def update(self):
        key_event = pygame.key.get_pressed()
        self.draw()

        for shooter in self.shooter:
            shooter.update(self.player, self.walls, not self.buttons[0].is_on)

        for button in self.buttons:
            button.update(self.player)

        for entity in self.entities:
            entity.update(self.player, self.entity_walls, self.doors)

        self.player.update(key_event, self.screen, self.entities, self.walls, self.falling_walls, self.doors)

        return self.room, self.door, self.screen


    def generate(self, player):
        self.player = player
        self.player.reset(self.player_spawn[0])

        for wall in self.walls:
            self.entity_walls.append(wall)
        for wall in self.falling_walls:
            self.entity_walls.append(wall)

        self.buttons.append(button.Button((7.4 * tile, 3 * tile), True, self.screen))

        self.entities.append(bug.Bug((7.4 * tile, 5 * tile), self.screen))


        self.shooter.append(stationary_shooter.Stationary_Shooter((18 * tile, 5 * tile), 'down', 32, self.screen))
        self.shooter.append(stationary_shooter.Stationary_Shooter((18 * tile, 10 * tile), 'up', 32, self.screen))

        # for shooter in self.shooter:
        #     self.entities.append(shooter)


    def falling_walls_generate(self):
        falling_walls = []

        for x in range(4):
            for y in range(4):
                falling_walls.append(wall.Wall(((x + 2) * tile, (y + 2) * tile)))

        for x in range(12):
            for y in range(4):
                falling_walls.append(wall.Wall(((x + 10) * tile, (y + 2) * tile)))

        for x in range(4):
            for y in range(4):
                falling_walls.append(wall.Wall(((x + 18) * tile, (y + 10) * tile)))

        for x in range(12):
            for y in range(4):
                falling_walls.append(wall.Wall(((x + 2) * tile, (y + 10) * tile)))

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
            case 16:
                self.door = 1
            case 18:
                self.door = 0
            case 23:
                self.door = 0



    def reset(self):
        del self.entities
        self.entities = []

        del self.shooter
        self.shooter = []

        self.generate(self.player)

        self.player.health = 3
