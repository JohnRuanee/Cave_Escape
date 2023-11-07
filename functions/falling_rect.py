import pygame

class Falling_Rect(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)

        self.rect = rect

        self.top_left = pygame.Rect(rect.top, rect.left, 1, 1)
        self.top_right = pygame.Rect(rect.top, rect.right - 1, 1, 1)
        self.bottom_left = pygame.Rect(rect.bottom - 1, rect.left, 1, 1)
        self.bottom_right = pygame.Rect(rect.bottom - 1, rect.right - 1, 1, 1)

    def check_collision(self, walls):
        fall_top_left_check = False
        fall_top_right_check = False
        fall_bottom_left_check = False
        fall_bottom_right_check = False


        for wall in walls:
            self.top_left.top = self.rect.top
            self.top_left.left = self.rect.left

            self.top_right.top = self.rect.top
            self.top_right.right = self.rect.right

            self.bottom_left.bottom = self.rect.bottom
            self.bottom_left.left = self.rect.left

            self.bottom_right.bottom = self.rect.bottom
            self.bottom_right.right = self.rect.right

            fall_top_left = pygame.Rect.colliderect(self.top_left, wall.rect)
            fall_top_right = pygame.Rect.colliderect(self.top_right, wall.rect)
            fall_bottom_left = pygame.Rect.colliderect(self.bottom_left, wall.rect)
            fall_bottom_right = pygame.Rect.colliderect(self.bottom_right, wall.rect)

            if fall_top_left:
                fall_top_left_check = True

            if fall_top_right:
                fall_top_right_check = True

            if fall_bottom_left:
                fall_bottom_left_check = True

            if fall_bottom_right:
                fall_bottom_right_check = True

        if fall_top_left_check and fall_top_right_check and fall_bottom_left_check and fall_bottom_right_check:
            return True
        else:
            return False

    def check_collision_doors(self, walls):
        for i in range(len(walls)):
            fall_top_left_check = False
            fall_top_right_check = False
            fall_bottom_left_check = False
            fall_bottom_right_check = False



            self.top_left.top = self.rect.top
            self.top_left.left = self.rect.left

            self.top_right.top = self.rect.top
            self.top_right.right = self.rect.right

            self.bottom_left.bottom = self.rect.bottom
            self.bottom_left.left = self.rect.left

            self.bottom_right.bottom = self.rect.bottom
            self.bottom_right.right = self.rect.right

            fall_top_left = pygame.Rect.colliderect(self.top_left, walls[i].rect)
            fall_top_right = pygame.Rect.colliderect(self.top_right, walls[i].rect)
            fall_bottom_left = pygame.Rect.colliderect(self.bottom_left, walls[i].rect)
            fall_bottom_right = pygame.Rect.colliderect(self.bottom_right, walls[i].rect)

            if fall_top_left:
                fall_top_left_check = True

            if fall_top_right:
                fall_top_right_check = True

            if fall_bottom_left:
                fall_bottom_left_check = True

            if fall_bottom_right:
                fall_bottom_right_check = True

            if fall_top_left_check and fall_top_right_check and fall_bottom_left_check and fall_bottom_right_check:
                return True, i

        return False, 999

