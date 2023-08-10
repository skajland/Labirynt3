import pygame
import gamestate
import time
import camera
from button import Button
import leveloader

# I'm making this game at the beginning of 14 years.
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode(camera.screen_size, pygame.FULLSCREEN)
pygame.display.set_caption('Labirynt 3')
start_button = Button("Play", (screen.get_width() / 2, screen.get_height() / 2), 96, (130, 130, 130, 70),
                      (75, 75, 75, 50), (160, 160, 160, 150))
menu_button = Button("Menu", (screen.get_width() / 2, screen.get_height() / 2 + 96), 96, (130, 130, 130, 70),
                     (75, 75, 75, 50), (160, 160, 160, 150))
exit_button = Button("Exit", (screen.get_width() / 2, screen.get_height() / 2 + 96), 96, (130, 130, 130, 70),
                     (75, 75, 75, 50), (160, 160, 160, 150))


def update():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gamestate.game_state = "Quitting"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                leveloader.load_map()
        gamestate.WorkShop.event_update(event)

    if leveloader.game_state == "Running":
        gamestate.Running.update()
    elif leveloader.game_state == "MainMenu":
        gamestate.MainMenu.update()
    elif leveloader.game_state == "DeathScreen":
        gamestate.DeathScreen.update()
    elif leveloader.game_state == "YouWin":
        gamestate.YouWin.update()


def render():
    if leveloader.game_state == "Running":
        gamestate.Running.render(screen)
    elif leveloader.game_state == "MainMenu":
        gamestate.MainMenu.render(screen)
    elif leveloader.game_state == "DeathScreen":
        gamestate.DeathScreen.render(screen)
    elif leveloader.game_state == "YouWin":
        gamestate.YouWin.render(screen)
    pygame.display.update()


dt = 16666667
currentime = time.time_ns()
accumulator = 0.0
while not leveloader.game_state == "Quitting":
    clock.tick(120)
    newtime = time.time_ns()
    frametime = newtime - currentime
    currentime = newtime
    accumulator += frametime
    while accumulator >= dt:
        update()
        accumulator -= dt
    render()
