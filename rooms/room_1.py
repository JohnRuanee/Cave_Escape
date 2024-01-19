import pygame
from functions import functions
from walls import breakable_wall, door, wall

tile = 16

class Room_1():
    def __init__(self, door_num, screen, player):
        self.door = door_num

        if self.door == 0:
            self.player_spawn = [(2.4 * tile, 6 * tile)]
        elif self.door == 1:
            self.player_spawn = [(20.6 * tile, 6 * tile)]
        else:
            self.player_spawn = [(13.4 * tile, 13 * tile)]

        self.falling_walls = self.falling_walls_generate()
        self.breakable_walls = []

        self.generate(player)
        self.buttons = []
        self.entities = []
        self.shooter = []

        self.walls = functions.make_walls(self.doors)
        for i in range(4):
            self.walls.append(self.breakable_walls[i])

        self.room = 1

        self.screen = screen

        self.adjacent_rooms = [0,2,11]

    def update(self):
        self.draw()
        key_event = pygame.key.get_pressed()

        for wall in self.breakable_walls:
            wall.update(self.player)

        self.player.update(key_event, self.screen, [], self.walls, self.falling_walls, self.doors)



        return self.room, self.door, self.screen

    def draw(self):
        image = pygame.image.load('map/images/Room_1.png')
        pygame.Surface.blit(self.screen, image, (0,0))


    def generate(self, player):
        self.player = player
        self.player.reset(self.player_spawn[0])

        self.doors = [door.Door((1.1 * tile, 6 * tile), 'right'), door.Door((22 * tile, 6 * tile), 'left'), door.Door((12 * tile, 14 * tile), 'down')]

        for i in range(4):
            self.breakable_walls.append(breakable_wall.Breakable_Wall(((12 + i) * tile, 12 * tile)))

    def falling_walls_generate(self):
        falling_walls = []
        for i in range(20):
            falling_walls.append(wall.Wall((i * tile + 2 * tile, 2 * tile)))
            falling_walls.append(wall.Wall((i * tile + 2 * tile, 3 * tile)))

        for i in range(4):
            falling_walls.append(wall.Wall((i * tile + 2 * tile, 4 * tile)))
            falling_walls.append(wall.Wall((i * tile + 2 * tile, 5 * tile)))

            falling_walls.append(wall.Wall((i * tile + 18 * tile, 10 * tile)))
            falling_walls.append(wall.Wall((i * tile + 18 * tile, 11 * tile)))

        falling_walls.append(wall.Wall((6 * tile + 2 * tile, 6 * tile)))
        falling_walls.append(wall.Wall((6 * tile + 2 * tile, 7 * tile)))
        falling_walls.append(wall.Wall((6 * tile + 2 * tile, 8 * tile)))
        falling_walls.append(wall.Wall((6 * tile + 2 * tile, 9 * tile)))
        falling_walls.append(wall.Wall((7 * tile + 2 * tile, 6 * tile)))
        falling_walls.append(wall.Wall((7 * tile + 2 * tile, 7 * tile)))
        falling_walls.append(wall.Wall((7 * tile + 2 * tile, 8 * tile)))
        falling_walls.append(wall.Wall((7 * tile + 2 * tile, 9 * tile)))

        for i in range(4):
            for j in range(4):
                falling_walls.append(wall.Wall((i * tile + 12 * tile, (6 + j) * tile)))

        for i in range(8):
            falling_walls.append(wall.Wall((i * tile + 2 * tile, 10 * tile)))
            falling_walls.append(wall.Wall((i * tile + 2 * tile, 11 * tile)))

        for i in range(6):
            falling_walls.append(wall.Wall((i * tile + 16 * tile, 12 * tile)))
            falling_walls.append(wall.Wall((i * tile + 16 * tile, 13 * tile)))

        for i in range(10):
            falling_walls.append(wall.Wall((i * tile + 2 * tile, 12 * tile)))
            falling_walls.append(wall.Wall((i * tile + 2 * tile, 13 * tile)))

            falling_walls.append(wall.Wall((i * tile + 12 * tile, 4 * tile)))
            falling_walls.append(wall.Wall((i * tile + 12 * tile, 5 * tile)))


        return falling_walls



    def room_door(self):

        return self.room, self.door

    def change_room(self, door):
        self.room = self.adjacent_rooms[door]
        self.door = 0

        match self.room:
            case 0:
                self.door = 1
            case 2:
                self.door = 0
            case 11:
                self.door = 0

    def reset(self):
        self.generate(self.player)
