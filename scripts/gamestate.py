import pygame
import leveloader
game_state = "Running"


class Running:
    @staticmethod
    def start():
        leveloader.level_maps = leveloader.load_map()

    @staticmethod
    def update():
        global game_state
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = "Quitting"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    leveloader.level_maps = leveloader.load_map()
        leveloader.update()

    @staticmethod
    def render(screen):
        screen.fill(leveloader.background_color)
        leveloader.render_level(screen)


class MainMenu:
    @staticmethod
    def update():
        pass

    @staticmethod
    def render(screen):
        pass


class DeathScreen:
    @staticmethod
    def update():
        pass

    @staticmethod
    def render(screen):
        pass
