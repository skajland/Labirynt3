import pygame.math
import camera
import leveloader
from button import Button

game_state = "MainMenu"
difficulty_multiplier = 1.15


class Running:

    @staticmethod
    def start():
        leveloader.load_map()

    @staticmethod
    def update():
        leveloader.update()

    @staticmethod
    def render(screen):
        screen.fill(leveloader.background_color)
        leveloader.render_level(screen)


class MainMenu:
    PlayButton = Button("Graj", pygame.Vector2(camera.screen_size[0] / 2, camera.screen_size[1] / 2 - 120), 128, (130, 130, 130, 70),
                    (130, 130, 130, 100),(160, 160, 160, 150))

    SettingsButton = Button("Ustawienia", pygame.math.Vector2(camera.screen_size[0] / 2, camera.screen_size[1] / 2), 128, (130, 130, 130, 70),
                    (130, 130, 130, 100),(160, 160, 160, 150))
    DifficultyButton = []
    ExitButton = Button("Exit", pygame.Vector2(camera.screen_size[0] / 2, camera.screen_size[1] / 2 + 120), 128, (130, 130, 130, 70),
                    (130, 130, 130, 100),(160, 160, 160, 150))
    DifficultyButton.append(
        Button("Easy", pygame.Vector2(camera.screen_size[0] / 2 - 250, camera.screen_size[1] / 2), 96,
               (130, 130, 130, 70),(130, 130, 130, 100), (160, 160, 160, 150), 0.95))
    DifficultyButton.append(
        Button("Medium", pygame.Vector2(camera.screen_size[0] / 2, camera.screen_size[1] / 2), 96,
               (130, 130, 130, 70),(130, 130, 130, 100), (160, 160, 160, 150), 1.15))
    DifficultyButton.append(
        Button("Hard", pygame.Vector2(camera.screen_size[0] / 2 + 250, camera.screen_size[1] / 2), 96,
               (130, 130, 130, 70),(130, 130, 130, 100), (160, 160, 160, 150), 1.3))

    @staticmethod
    def update():
        MainMenu.PlayButton.collision(MainMenu.change_game_state)
        MainMenu.ExitButton.collision(MainMenu.game_exit)
        bigger_rect = pygame.Rect(MainMenu.SettingsButton.rect.x - 90, MainMenu.SettingsButton.rect.y, MainMenu.SettingsButton.rect.width + 180,
                                  MainMenu.SettingsButton.rect.height)
        if not bigger_rect.collidepoint(pygame.mouse.get_pos()):
            MainMenu.SettingsButton.collision(MainMenu.change_game_state)
            return
        for button in MainMenu.DifficultyButton:
            button.collision(MainMenu.change_difficulty)

    @staticmethod
    def game_exit():
        global game_state
        game_state = "Quitting"

    @staticmethod
    def change_difficulty(multiplier):
        global difficulty_multiplier
        difficulty_multiplier = multiplier[0]

    @staticmethod
    def render(screen):
        screen.fill(leveloader.background_color)
        MainMenu.PlayButton.render(screen)
        MainMenu.ExitButton.render(screen)
        bigger_rect = pygame.Rect(MainMenu.SettingsButton.rect.x - 90, MainMenu.SettingsButton.rect.y, MainMenu.SettingsButton.rect.width + 180,
                                  MainMenu.SettingsButton.rect.height)
        if not bigger_rect.collidepoint(pygame.mouse.get_pos()):
            MainMenu.SettingsButton.render(screen)
            return
        for button in MainMenu.DifficultyButton:
            button.render(screen)

    @staticmethod
    def change_game_state():
        global game_state
        game_state = "Running"


class DeathScreen:
    @staticmethod
    def update():
        pass

    @staticmethod
    def render(screen):
        screen.fill(leveloader.background_color)
