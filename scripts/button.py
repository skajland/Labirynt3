import pygame
pygame.init()


class Button:

    def __init__(self, what_to_say, pos, font_size, default_color, button_hovering_color, button_pressed_color, *func_arguments):
        self.func_arguments = func_arguments
        self.default_color = default_color
        self.button_hovering_color = button_hovering_color
        self.button_pressed_color = button_pressed_color
        self.font = pygame.font.Font(None, font_size)
        if not type(what_to_say) == pygame.Surface:
            self.rendered_font = self.font.render(what_to_say, True, 'Black')
            self.rect = self.rendered_font.get_rect()
            self.rect.center = pos
            self.isimage = False
        else:
            self.isimage = True
            self.image = what_to_say
            self.rect = self.image.get_rect()
            self.rect.center = pos
        self.button_state = "None"
        self.mouse_down = False

    def collision(self, func):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.button_state = "Hovering"
            self.collision_checker(func)
        else:
            self.button_state = "None"

    def collision_checker(self, func):
        if pygame.mouse.get_pressed()[0]:
            func(*self.func_arguments)
            self.button_state = "Pressed"
            self.mouse_down = True
            return
        self.mouse_down = False

    def render(self, screen):
        if self.isimage:
            surf = pygame.Surface((self.rect.w, self.rect.h)).convert_alpha()
            screen.blit(self.image, self.rect)
        else:
            surf = pygame.Surface((self.rect.w, self.rect.h)).convert_alpha()
            screen.blit(self.rendered_font, self.rect)
        if self.button_state == "Pressed":
            surf.fill(self.button_pressed_color)
        elif self.button_state == "Hovering":
            surf.fill(self.button_hovering_color)
        else:
            surf.fill(self.default_color)
        screen.blit(surf, self.rect)
