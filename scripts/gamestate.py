import os
import usefull
import pygame.math
import camera
import gamedata
import leveloader

font = pygame.font.Font(None, 172)


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
                              0),
        usefull.create_button("Medium", pygame.Vector2(camera.screen_size[0] / 2, camera.screen_size[1] / 2), 96, 1),
        usefull.create_button("Hard", pygame.Vector2(camera.screen_size[0] / 2 + 250, camera.screen_size[1] / 2), 96,
                              2)]
    font_rendered = font.render("Labirynt 3", True, (20, 165, 20))
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
        leveloader.game_state = "Quitting"

    @staticmethod
    def change_difficulty(*multiplier):
        leveloader.current_difficulty = multiplier[0]

    @staticmethod
    def render(screen):
        screen.fill(leveloader.background_color)
        if MainMenu.workshop_enabled:
            WorkShop.render(screen)
            return
        screen.blit(MainMenu.font_rendered, (screen.get_width() / 2 - MainMenu.font_rendered.get_width() / 2, 100))
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
        gamedata.levels = gamedata.original_levels
        gamedata.levels_data = gamedata.original_data
        gamedata.current_level = 0
        leveloader.load_map()
        leveloader.game_state = "Running"


class WorkShop:
    sub_folders = []
    workshop_offset = pygame.Vector2()
    scale = (64, 64)
    menu_button = usefull.create_button(pygame.transform.scale(pygame.image.load(usefull.data_directory + "res/ExitButton.png"), scale),
                                        pygame.Vector2(scale[0] / 2, scale[1] / 2), 128)

    @staticmethod
    def detect_sub_folders():
        sub_folders = [folder for folder in os.listdir(usefull.data_directory + "Workshop/") if
                       os.path.isdir(usefull.data_directory + "Workshop/" + folder)]
        return sub_folders

    @staticmethod
    def update():
        WorkShop.sub_folders = WorkShop.detect_sub_folders()
        WorkShop.menu_button.collision(WorkShop.menu)

    @staticmethod
    def menu():
        MainMenu.workshop_enabled = False

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
            collection_button = usefull.create_button(sub_folder, pygame.Vector2(screen.get_width() / 2, 96 * (
                        i + 1)) + WorkShop.workshop_offset,
                                                      96, sub_folder)
            collection_button.collision(WorkShop.load_collection)
            collection_button.render(screen)
        WorkShop.menu_button.render(screen)

    @staticmethod
    def load_collection(collection):
        collection_path = [folder for folder in os.listdir(usefull.data_directory + "Workshop/" + collection) if
                           os.path.isdir(usefull.data_directory + "Workshop/" + collection + "/" + folder)]
        levels_path = [usefull.data_directory + "Workshop/" + collection + "/" + level_path + "/level" for level_path in collection_path]
        levels_data_path = [usefull.data_directory + "Workshop/" + collection + "/" + level_path + "/leveldata" for level_path in
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
        leveloader.game_state = "Running"
        MainMenu.workshop_enabled = False


class DeathScreen:
    PlayButton = usefull.create_button("Graj",
                                       pygame.Vector2(camera.screen_size[0] / 2, camera.screen_size[1] / 2 - 60), 128)
    MenuButton = usefull.create_button("Menu",
                                       pygame.Vector2(camera.screen_size[0] / 2, camera.screen_size[1] / 2 + 60), 128)
    font_rendered = font.render("Zginoles", True, (20, 165, 20))

    @staticmethod
    def update():
        DeathScreen.PlayButton.collision(DeathScreen.reset_game)
        DeathScreen.MenuButton.collision(DeathScreen.menu)

    @staticmethod
    def menu():
        leveloader.game_state = "MainMenu"

    @staticmethod
    def reset_game():
        gamedata.current_level = 0
        leveloader.load_map()
        leveloader.game_state = "Running"

    @staticmethod
    def render(screen):
        screen.fill(leveloader.background_color)
        screen.blit(DeathScreen.font_rendered,
                    (screen.get_width() / 2 - DeathScreen.font_rendered.get_width() / 2, 100))
        DeathScreen.PlayButton.render(screen)
        DeathScreen.MenuButton.render(screen)


class YouWin:
    PlayButton = usefull.create_button("Graj",
                                       pygame.Vector2(camera.screen_size[0] / 2, camera.screen_size[1] / 2 - 60), 128)
    MenuButton = usefull.create_button("Menu",
                                       pygame.Vector2(camera.screen_size[0] / 2, camera.screen_size[1] / 2 + 60), 128)
    font_rendered = font.render("Wygrales", True, (20, 165, 20))

    @staticmethod
    def update():
        YouWin.PlayButton.collision(DeathScreen.reset_game)
        YouWin.MenuButton.collision(DeathScreen.menu)

    @staticmethod
    def menu():
        leveloader.game_state = "MainMenu"

    @staticmethod
    def reset_game():
        gamedata.current_level = 0
        leveloader.load_map()
        leveloader.game_state = "Running"

    @staticmethod
    def render(screen):
        screen.fill(leveloader.background_color)
        screen.blit(YouWin.font_rendered,
                    (screen.get_width() / 2 - YouWin.font_rendered.get_width() / 2, 100))
        YouWin.PlayButton.render(screen)
        YouWin.MenuButton.render(screen)
