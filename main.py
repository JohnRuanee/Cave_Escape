import pygame

from functions import functions
from entities import player

pygame.init()

tile = 16

room_width = 24
room_height = 16

screen_multiple = 2

screen_width = tile * room_width * screen_multiple
screen_height = tile * room_height * screen_multiple

window = pygame.display.set_mode([screen_width, screen_height])
screen = pygame.Surface([tile * room_width, tile * room_height])


def draw():
    frame = pygame.transform.scale(screen, (screen_width, screen_height))
    window.blit(frame, frame.get_rect())
    pygame.display.flip()


# screen = pygame.display.set_mode((screen_width, screen_height))
# draw_screen = pygame.display.set_mode((160, 160))
pygame.display.set_caption("Cave escape")

# set up refresh rate
clock = pygame.time.Clock()

# current room and door
room = 0
door = 0

# game loop boolean
game_over = False
new_room = False

player = player.Player((0, 0))

player.can_attack = False

curr_room = functions.room_picker(room, door, screen, player)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    new_room, door = curr_room.room_door()

    if new_room != room:
        room = new_room

        curr_room = functions.room_picker(room, door, screen, player)

    if player.health == 0:
        curr_room = functions.room_picker(room, door, screen, player)
        player.health = 3

    curr_room.update()

    screen_rect = pygame.rect.Rect(0,0,screen_width,screen_height)

    functions.draw_hitbox(curr_room)
    functions.draw_sprites(curr_room)

    if room == 0 and player.can_attack:
        pygame.font.init()
        my_font = pygame.font.SysFont(None, 30)

        text_surface = my_font.render('Created By: John Ruane', False, (250,250,250))

        screen.blit(text_surface, (32,0))

    draw()

    pygame.display.flip()
    clock.tick(20)


