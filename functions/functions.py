from walls import wall
from rooms import (room_99, room_1, room_2, room_0, room_3, room_4, room_5, room_6, room_7, room_8, room_9, room_10,
                   room_11, room_12, room_13, room_14, room_24, room_15, room_16, room_17, room_23, room_25, room_26)

tile = 16


def room_picker(room, door, screen, player):

    curr_room = room_99.Room_99(door, screen, player)

    match room:
        case 99:
            curr_room = room_99.Room_99(door, screen, player)
        case 0:
            curr_room = room_0.Room_0(door, screen, player)
        case 1:
            curr_room = room_1.Room_1(door, screen, player)
        case 2:
            curr_room = room_2.Room_2(door, screen, player)
        case 3:
            curr_room = room_3.Room(door, screen, player)
        case 4:
            curr_room = room_4.Room(door, screen, player)
        case 5:
            curr_room = room_5.Room(door, screen, player)
        case 6:
            curr_room = room_6.Room(door, screen, player)
        case 7:
            curr_room = room_7.Room(door, screen, player)
        case 8:
            curr_room = room_8.Room(door, screen, player)
        case 9:
            curr_room = room_9.Room(door, screen, player)
        case 10:
            curr_room = room_10.Room(door, screen, player)
        case 11:
            curr_room = room_11.Room(door, screen, player)
        case 12:
            curr_room = room_12.Room(door, screen, player)
        case 13:
            curr_room = room_13.Room(door, screen, player)
        case 14:
            curr_room = room_14.Room(door, screen, player)
        case 15:
            curr_room = room_15.Room(door, screen, player)
        case 16:
            curr_room = room_16.Room(door, screen, player)
        case 17:
            curr_room = room_17.Room(door, screen, player)

        case 23:
            curr_room = room_23.Room(door, screen, player)
        case 24:
            curr_room = room_24.Room(door, screen, player)
        case 25:
            curr_room = room_25.Room(door, screen, player)
        case 26:
            curr_room = room_26.Room(door, screen, player)

    player.set_room(curr_room)

    return curr_room


def make_walls(doors):
    walls = []

    for i in range(24):
        walls.append(wall.Wall((i * tile, 0)))
    for i in range(24):
        walls.append(wall.Wall((i * tile, tile * 15)))
    for i in range(16):
        walls.append(wall.Wall((0, tile * i)))
    for i in range(16):
        walls.append(wall.Wall((23 * tile, tile * i)))

    for i in range(22):
        x = i * tile + tile
        y = tile
        can_wall = check_door(x, y, doors)
        if can_wall:
            walls.append(wall.Wall((x, y)))
    for i in range(22):
        x = i * tile + tile
        y = tile * 14
        can_wall = check_door(x, y, doors)
        if can_wall:
            walls.append(wall.Wall((x, y)))
    for i in range(14):
        x = tile
        y = tile * i + tile
        can_wall = check_door(x, y, doors)
        if can_wall:
            walls.append(wall.Wall((x, y)))
    for i in range(14):
        x = 22 * tile
        y = tile * i + tile
        can_wall = check_door(x, y, doors)
        if can_wall:
            walls.append(wall.Wall((x, y)))

    return walls

def check_door(x, y, doors):
    can_wall = True
    for door in doors:
        if door.facing == 'left' or door.facing == 'right':
            if (door.rect.x - x <= tile and (y - door.rect.y <= 3 * tile and y >= door.rect.y)):
                can_wall = False
        else:
            if ((x - door.rect.x <= 4 * tile and x >= door.rect.x) and abs(door.rect.y - y <= tile)):
                can_wall = False
    return can_wall
