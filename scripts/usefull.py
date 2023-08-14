import pygame

import button
import os

working_directory = os.getcwd()
working_directory_split = working_directory.split('/')
global_directory = ''.join(["/" + add for add in working_directory_split[1:-1]]) + "/"
data_directory = global_directory + "data/"

mainMenuMusic = pygame.mixer.Sound(data_directory + "Sounds/MainMenuMusic.wav")
mainMenuMusic.play(-1)
playingMusic = pygame.mixer.Sound(data_directory + "Sounds/PlayingMusic.wav")
playingMusic.set_volume(0.5)
button_highlight_sound = pygame.mixer.Sound(data_directory + "Sounds/ButtonHighlight.wav")
button_press_sound = pygame.mixer.Sound(data_directory + "Sounds/ButtonPress.wav")
DeathMusic = pygame.mixer.Sound(data_directory + "Sounds/DeathMusic.wav")
turret_shoot_sound = pygame.mixer.Sound(data_directory + "Sounds/TurretShoot.wav")
coins_collect = pygame.mixer.Sound(data_directory + "Sounds/CoinsCollect.wav")


def create_button(what_to_say, pos, font_size, *func_arguments):
    return button.Button(what_to_say, pos, font_size,
                         (130, 130, 130, 70), (130, 130, 130, 100), (160, 160, 160, 150), *func_arguments)
