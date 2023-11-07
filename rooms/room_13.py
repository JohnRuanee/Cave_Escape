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
            self.player_spawn = [(17.4 * tile, 2.4 * tile)]
        elif self.door == 1:
            self.player_spawn = [(20.4 * tile, 7.4 * tile)]
        else:
            self.player_spawn = [(5.4 * tile, 12.6 * tile)]

        self.falling_walls = self.falling_walls_generate()

        self.doors = [door.Door((16 * tile, 1 * tile), 'down'), door.Door((22 * tile, 6 * tile), 'left'), door.Door((4 * tile, 13.8 * tile), 'down')]

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

        self.room = 13

        self.adjacent_rooms = [12,14,24]

    def update(self):
        key_event = pygame.key.get_pressed()
        self.draw_hitbox()

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

        self.entities.append(bat.Bat((5.4 * tile, 7.4 * tile), self.screen))
        self.entities.append(bat.Bat((11.4 * tile, 7.4 * tile), self.screen))
        self.entities.append(bat.Bat((17.4 * tile, 7.4 * tile), self.screen))

        self.entities.append(bat.Bat((17.4 * tile, 10.4 * tile), self.screen))
        self.entities.append(bat.Bat((11.4 * tile, 10.4 * tile), self.screen))

        self.entities.append(bat.Bat((11.4 * tile, 4.4 * tile), self.screen))
        self.entities.append(bat.Bat((5.4 * tile, 4.4 * tile), self.screen))


    def falling_walls_generate(self):
        falling_walls = []

        # for x in range(2):
        #     for y in range(12):
        #         falling_walls.append(wall.Wall(((x + 2) * tile, (y + 2) * tile)))
        #
        # for x in range(2):
        #     for y in range(12):
        #         falling_walls.append(wall.Wall(((x + 20) * tile, (y + 2) * tile)))
        #
        # for x in range(12):
        #     for y in range(4):
        #         falling_walls.append(wall.Wall(((x + 4) * tile, (y + 10) * tile)))
        #
        # for x in range(12):
        #     for y in range(4):
        #         falling_walls.append(wall.Wall(((x + 8) * tile, (y + 2) * tile)))

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
            case 12:
                self.door = 1
            case 14:
                self.door = 0
            case 24:
                self.door = 0


    def reset(self):
        del self.entities
        self.entities = []

        self.generate(self.player)

        self.player.health = 3