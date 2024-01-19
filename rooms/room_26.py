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
            self.player_spawn = [(2.4 * tile, 7.4 * tile)]
        elif self.door == 1:
            self.player_spawn = [(17.4 * tile, 2.4 * tile)]
        else:
            self.player_spawn = [(20.4 * tile, 7.4 * tile)]

        self.falling_walls = self.falling_walls_generate()

        self.doors = [door.Door((1 * tile, 6 * tile), 'left'),
                      door.Door((16 * tile, 1 * tile), 'down'),
                      door.Door((22 * tile, 6 * tile), 'left')]

        self.shooter = []
        self.buttons = []
        self.breakable_walls = []
        self.entity_walls = []

        self.walls = functions.make_walls(self.doors)
        for i in range(5):
            self.walls.append(wall.Wall(((16 + i) * tile, 14 * tile)))
            # self.walls.append(wall.Wall(((22) * tile, (6 + i) * tile)))

        self.entities = []

        self.generate(player)

        self.button_bool = True

        self.room = 26

        self.adjacent_rooms = [25,27,21]

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

        self.entities.append(bat.Bat((5 * tile, 5 * tile), self.screen))
        self.entities.append(bat.Bat((5 * tile, 10 * tile), self.screen))

        self.entities.append(bug.Bug((7 * tile, 6 * tile), self.screen))
        self.entities.append(bug.Bug((7 * tile, 9 * tile), self.screen))

        self.entities.append(bat.Bat((18 * tile, 5 * tile), self.screen))
        self.entities.append(bat.Bat((18 * tile, 10 * tile), self.screen))

        self.entities.append(bug.Bug((16 * tile, 6 * tile), self.screen))
        self.entities.append(bug.Bug((16 * tile, 9 * tile), self.screen))

        self.entities.append(bat.Bat((15 * tile, 3 * tile), self.screen))
        self.entities.append(bat.Bat((20 * tile, 3 * tile), self.screen))

        self.entities.append(bug.Bug((7 * tile, 6 * tile), self.screen))
        self.entities.append(bug.Bug((7 * tile, 9 * tile), self.screen))

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
            case 25:
                self.door = 1
            case 27:
                self.door = 0
            case 21:
                self.door = 4



    def reset(self):
        del self.entities
        self.entities = []

        del self.shooter
        self.shooter = []

        self.generate(self.player)

        self.player.health = 3
