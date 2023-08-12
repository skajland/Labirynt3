import pygame
import gamestate
pygame.init()
pressed = False


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
            if self.button_state == "None" and not self.mouse_down:
                gamestate.button_highlight_sound.play()
            self.button_state = "Hovering"
            self.collision_checker(func)
        else:
            self.button_state = "None"

    def collision_checker(self, func):
        global pressed
        if pygame.mouse.get_pressed()[0]:
            self.button_state = "Pressed"
            if pressed:
                return
            pressed = True
            gamestate.button_press_sound.play()
            func(*self.func_arguments)
            self.mouse_down = True
            return
        elif not pygame.mouse.get_pressed()[0] and pressed:
            pressed = False
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
