import pygame
import gamestate
import time
import camera
from button import Button
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode(camera.screen_size)
pygame.display.set_caption('Labirynt 3')

start_button = Button("Play", (screen.get_width() / 2, screen.get_height() / 2), 96, (130, 130, 130, 70),
                      (75, 75, 75, 50), (160, 160, 160, 150))
menu_button = Button("Menu", (screen.get_width() / 2, screen.get_height() / 2 + 96), 96, (130, 130, 130, 70),
                     (75, 75, 75, 50), (160, 160, 160, 150))
exit_button = Button("Exit", (screen.get_width() / 2, screen.get_height() / 2 + 96), 96, (130, 130, 130, 70),
                     (75, 75, 75, 50), (160, 160, 160, 150))
gamestate.Running.start()


def update():
    if gamestate.game_state == "Running":
        gamestate.Running.update()
    elif gamestate.game_state == "MainMenu":
        gamestate.MainMenu.update()
    elif gamestate.game_state == "DeathScreen":
        gamestate.DeathScreen.update()


def render():

    if gamestate.game_state == "Running":
        gamestate.Running.render(screen)
    elif gamestate.game_state == "MainMenu":
        gamestate.MainMenu.render(screen)
    elif gamestate.game_state == "DeathScreen":
        gamestate.DeathScreen.render(screen)
    pygame.display.update()



dt = 16666667
currentime = time.time_ns()
accumulator = 0.0
while not gamestate.game_state == "Quitting":
    clock.tick(165)
    newtime = time.time_ns()
    frametime = newtime - currentime
    currentime = newtime
    accumulator += frametime
    while accumulator >= dt:
        update()
        accumulator -= dt
    render()
