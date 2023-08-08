import pygame

left = 258
top = 258
right = 258
bottom = 258
offset = pygame.math.Vector2()
screen_size = (1462, 946)


def box_camera(rect):
    global offset
    box_rect = pygame.Rect(left, top, screen_size[0] - (right + left), screen_size[1] - (bottom + top))
    if rect.left < box_rect.left:
        rect.left = box_rect.left
        offset.x += 86
    if rect.right > box_rect.right:
        rect.right = box_rect.right
        offset.x += -86
    if rect.top < box_rect.top:
        rect.top = box_rect.top
        offset.y += 86
    if rect.bottom > box_rect.bottom:
        rect.bottom = box_rect.bottom
        offset.y += -86


def rect_checker(rect, size_offset):
    global offset
    box_rect = pygame.Rect(-size_offset[0], -size_offset[1], screen_size[0] + size_offset[0] * 2, screen_size[1] + size_offset[1] * 2)
    if rect.left < box_rect.left or rect.right > box_rect.right or rect.top < box_rect.top or rect.bottom > box_rect.bottom:
        return True
    return False
