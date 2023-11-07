# -*- coding: utf-8 -*-

import pygame
from entities import bat, player, bug
from walls import button, stationary_shooter, wall

pygame.init()

tile = 16

room_size = 16

screen_multiple = 2

screen_width    = tile * room_size * screen_multiple
screen_height   = tile * room_size * screen_multiple

window = pygame.display.set_mode([screen_width, screen_height])
screen = pygame.Surface([tile * room_size, tile * room_size])

def draw():
    frame = pygame.transform.scale(screen, (screen_width, screen_height))
    window.blit(frame, frame.get_rect())
    pygame.display.flip()


#screen = pygame.display.set_mode((screen_width, screen_height))
#draw_screen = pygame.display.set_mode((160, 160))
pygame.display.set_caption("Cave escape")



#set up refresh rate
clock = pygame.time.Clock()

#character position
player = player.Player((16, 16))

bug = bug.Bug((80, 80), screen)
bat = bat.Bat((100, 100), screen)
shooter = stationary_shooter.Stationary_Shooter((tile * 8, tile * 3), 'left', screen)
button = button.Button((tile * 8, tile * 6), True, screen)

entities = pygame.sprite.Group()
players = pygame.sprite.Group()
walls = []
enemy_walls = []
falling_walls = []

for i in range(16):
    walls.append(wall.Wall((i * tile, 0)))
for i in range(16):
    walls.append(wall.Wall((i * tile, tile * 15 + 2)))
for i in range(16):
    walls.append(wall.Wall((0, tile * i)))
for i in range(16):
    walls.append(wall.Wall((15 * tile + 2, tile * i)))


all_sprites = pygame.sprite.Group()

players.add(player)
all_sprites.add(player)

entities.add(bug)
all_sprites.add(bug)

entities.add(bat)
all_sprites.add(bat)

all_sprites.add(shooter)
walls.append(shooter)

enemy_walls.append(button)

falling_walls.append(wall.Wall((5 * tile, 5 * tile)))
falling_walls.append(wall.Wall((5 * tile, 6 * tile), ))
falling_walls.append(wall.Wall((6 * tile, 5 * tile)))
falling_walls.append(wall.Wall((6 * tile, 6 * tile)))




def collision():
    test = False

#game loop boolean
game_over = False

while game_over == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    screen.fill((250,250,250))

    for wall in walls:
        pygame.draw.rect(screen, wall.color, wall.rect)

    key_event = pygame.key.get_pressed()
    player.update(key_event, screen, entities, walls, falling_walls)
    bug.update(player, walls, enemy_walls)
    bat.update(player, walls, enemy_walls)
    button.update(player)
    shooter.update(player, walls, not button.is_on)


    #screen.blit(player.image, player.rect)
    pygame.draw.rect(screen, player.color, player.rect)
    pygame.draw.rect(screen, bug.color, bug.rect)
    pygame.draw.rect(screen, bat.color, bat.rect)
    pygame.draw.rect(screen, (255, 0, 0), shooter.rect)
    pygame.draw.rect(screen, (0 ,255, 255), button.rect)

    pygame.draw.rect(screen, (0,0,255), player.buffer_rect_left)
    pygame.draw.rect(screen, (0, 0, 255), player.buffer_rect_right)
    pygame.draw.rect(screen, (0, 0, 255), player.buffer_rect_up)
    pygame.draw.rect(screen, (0, 0, 255), player.buffer_rect_down)

    pygame.draw.rect(screen, (0,0,0), bug.collision_rect)

    for wall in falling_walls:
        pygame.draw.rect(screen, (0, 255, 50), wall.rect)

    health_text = pygame.font.SysFont(None, tile).render(str(player.health), 1, (255, 255, 255))
    screen.blit(health_text, (4, 4))

    draw()
    #screen.blit(pygame.transform.scale(draw_screen, (screen_width, screen_height)), (0,0))

    pygame.display.flip()
    clock.tick(20)

pygame.quit()


