import pygame

from entities import bug, bat
from walls import button, door, stationary_shooter, wall
from functions import functions

tile = 16

class Room():
    def __init__(self, door_num, screen, player):
        self.door = door_num

        self.screen = screen

        if self.door == 1:
            self.player_spawn = [(15.4 * tile, 11.4 * tile)]
        else:
            self.player_spawn = [(2.4 * tile, 7.4 * tile)]

        self.falling_walls = self.falling_walls_generate()

        self.doors = [door.Door((1 * tile, 6 * tile), 'left'), door.Door((14 * tile, 13.8 * tile), 'down')]

        self.shooter = []
        self.buttons = []
        self.breakable_walls = []
        self.entity_walls = []

        self.walls = functions.make_walls(self.doors)
        for i in range(5):
            self.walls.append(wall.Wall(((10 + i) * tile, 1 * tile)))
            self.walls.append(wall.Wall(((9 + i) * tile, 14 * tile)))
            self.walls.append(wall.Wall(((22) * tile, (6 + i) * tile)))

        self.entities = []

        self.generate(player)

        self.button_bool = True

        self.room = 18

        self.adjacent_rooms = [17,19]

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

        self.buttons.append(button.Button((19 * tile, 12 * tile), True, self.screen))

        for i in range(12):
            self.shooter.append(stationary_shooter.Stationary_Shooter((21 * tile, (i + 2) * tile), 'left', 4, self.screen))

        # for shooter in self.shooter:
        #     self.entities.append(shooter)


    def falling_walls_generate(self):
        falling_walls = []

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

        for shooter in self.shooter:
            pygame.draw.rect(self.screen, (255, 0,0), shooter.rect)



    def room_door(self):

        return self.room, self.door

    def change_room(self, door):
        self.room = self.adjacent_rooms[door]
        self.door = 0

        match self.room:
            case 17:
                self.door = 1
            case 19:
                self.door = 0

    def reset(self):
        del self.entities
        self.entities = []

        del self.shooter
        self.shooter = []

        self.generate(self.player)

        self.player.health = 3
