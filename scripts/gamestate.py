import os
import usefull
import pygame.math
import camera
import gamedata
import leveloader

game_state = "MainMenu"
difficulty_multiplier = 1


class Running:

    @staticmethod
    def update():
        leveloader.update()

    @staticmethod
    def render(screen):
        screen.fill(leveloader.background_color)
        leveloader.render_level(screen)


class MainMenu:
    PlayButton = usefull.create_button("Graj",
                                       pygame.Vector2(camera.screen_size[0] / 2, camera.screen_size[1] / 2 - 120), 128)

    SettingsButton = usefull.create_button("Ustawienia",
                                           pygame.Vector2(camera.screen_size[0] / 2, camera.screen_size[1] / 2), 128)
    Workshop = usefull.create_button("Workshop",
                                     pygame.Vector2(camera.screen_size[0] / 2, camera.screen_size[1] / 2 + 120), 128)
    ExitButton = usefull.create_button("Wyjc",
                                       pygame.Vector2(camera.screen_size[0] / 2, camera.screen_size[1] / 2 + 240), 128)
    DifficultyButtons = [
        usefull.create_button("Easy", pygame.Vector2(camera.screen_size[0] / 2 - 250, camera.screen_size[1] / 2), 96,
                              0.7),
        usefull.create_button("Medium", pygame.Vector2(camera.screen_size[0] / 2, camera.screen_size[1] / 2), 96, 1),
        usefull.create_button("Hard", pygame.Vector2(camera.screen_size[0] / 2 + 250, camera.screen_size[1] / 2), 96,
                              1.35)]
    workshop_enabled = False

    @staticmethod
    def update():
        if MainMenu.workshop_enabled:
            WorkShop.update()
            return
        WorkShop.workshop_offset = pygame.Vector2()
        MainMenu.PlayButton.collision(MainMenu.change_game_state)
        MainMenu.Workshop.collision(MainMenu.workshop_activate)
        MainMenu.ExitButton.collision(MainMenu.game_exit)
        bigger_rect = pygame.Rect(MainMenu.SettingsButton.rect.x - 90, MainMenu.SettingsButton.rect.y,
                                  MainMenu.SettingsButton.rect.width + 180,
                                  MainMenu.SettingsButton.rect.height)
        if not bigger_rect.collidepoint(pygame.mouse.get_pos()):
            MainMenu.SettingsButton.collision(MainMenu.change_game_state)
            return
        for button in MainMenu.DifficultyButtons:
            button.collision(MainMenu.change_difficulty)

    @staticmethod
    def workshop_activate():
        MainMenu.workshop_enabled = not MainMenu.workshop_enabled

    @staticmethod
    def game_exit():
        global game_state
        game_state = "Quitting"

    @staticmethod
    def change_difficulty(*multiplier):
        global difficulty_multiplier
        difficulty_multiplier = multiplier[0]

    @staticmethod
    def render(screen):
        screen.fill(leveloader.background_color)
        if MainMenu.workshop_enabled:
            WorkShop.render(screen)
            return
        MainMenu.PlayButton.render(screen)
        MainMenu.Workshop.render(screen)
        MainMenu.ExitButton.render(screen)
        bigger_rect = pygame.Rect(MainMenu.SettingsButton.rect.x - 90, MainMenu.SettingsButton.rect.y,
                                  MainMenu.SettingsButton.rect.width + 180,
                                  MainMenu.SettingsButton.rect.height)
        if not bigger_rect.collidepoint(pygame.mouse.get_pos()):
            MainMenu.SettingsButton.render(screen)
            return
        for button in MainMenu.DifficultyButtons:
            button.render(screen)

    @staticmethod
    def change_game_state():
        global game_state
        gamedata.levels = gamedata.original_levels
        gamedata.levels_data = gamedata.original_data
        gamedata.current_level = 0
        leveloader.load_map()
        game_state = "Running"


class WorkShop:
    sub_folders = []
    prev_mouse_pos = pygame.mouse.get_pos()
    workshop_offset = pygame.Vector2()

    @staticmethod
    def detect_sub_folders():
        sub_folders = [folder for folder in os.listdir("Workshop/") if
                       os.path.isdir("Workshop/" + folder)]
        return sub_folders

    @staticmethod
    def update():
        WorkShop.sub_folders = WorkShop.detect_sub_folders()

    @staticmethod
    def event_update(event):
        speed = 25
        if not MainMenu.workshop_enabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                WorkShop.workshop_offset.y -= speed
            if event.button == 5 and WorkShop.workshop_offset.y <= 0 - speed:
                WorkShop.workshop_offset.y += speed

    @staticmethod
    def render(screen):
        for i, sub_folder in enumerate(WorkShop.sub_folders):
            collection_button = usefull.create_button(sub_folder, pygame.Vector2(screen.get_width() / 2, 96 * (i + 1)) + WorkShop.workshop_offset,
                                                      96, sub_folder)
            collection_button.collision(WorkShop.load_collection)
            collection_button.render(screen)

    @staticmethod
    def load_collection(collection):
        global game_state
        collection_path = [folder for folder in os.listdir("Workshop/" + collection) if
                           os.path.isdir("Workshop/" + collection + "/" + folder)]
        levels_path = ["Workshop/" + collection + "/" + level_path + "/level" for level_path in collection_path]
        levels_data_path = ["Workshop/" + collection + "/" + level_path + "/leveldata" for level_path in
                            collection_path]
        if len(levels_path) <= 0 or len(levels_data_path) <= 0:
            return
        for level_path in levels_path:
            if not os.path.exists(level_path) or not os.path.isfile(level_path):
                return
        for level_data_path in levels_data_path:
            if not os.path.exists(level_data_path) or not os.path.isfile(level_data_path):
                return
        gamedata.current_level = 0
        gamedata.levels = levels_path
        gamedata.levels_data = levels_data_path
        leveloader.load_map()
        game_state = "Running"
        MainMenu.workshop_enabled = False


class DeathScreen:
    PlayButton = usefull.create_button("Graj",
                                       pygame.Vector2(camera.screen_size[0] / 2, camera.screen_size[1] / 2 - 60), 128)
    MenuButton = usefull.create_button("Menu",
                                       pygame.Vector2(camera.screen_size[0] / 2, camera.screen_size[1] / 2 + 60), 128)

    @staticmethod
    def update():
        DeathScreen.PlayButton.collision(DeathScreen.reset_game)
        DeathScreen.MenuButton.collision(DeathScreen.menu)

    @staticmethod
    def menu():
        global game_state
        game_state = "MainMenu"

    @staticmethod
    def reset_game():
        global game_state
        gamedata.current_level = 0
        leveloader.load_map()
        game_state = "Running"

    @staticmethod
    def render(screen):
        screen.fill(leveloader.background_color)
        DeathScreen.PlayButton.render(screen)
        DeathScreen.MenuButton.render(screen)
