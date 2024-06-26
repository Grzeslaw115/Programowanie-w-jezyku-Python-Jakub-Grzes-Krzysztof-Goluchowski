import pygame
from sys import exit
from settingsLoader import load_settings, reset_to_default
from levelSelection import main as levelSelection
from settingsPanel import main as settingsPanel
from button import Button
from HallOfFame import main as hallOfFame

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Load settings
reset_to_default()
settings = load_settings()

# Screen setup
SCREEN_WIDTH = settings['SCREEN_WIDTH']
SCREEN_HEIGHT = settings['SCREEN_HEIGHT']
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Miners' Bastion")

# Load fonts, music, and sounds
title_font = pygame.font.Font("assets/fonts/heav.ttf", 128)
pygame.mixer.music.load("assets/audio/menu/menu.mp3")
button_click_sound = pygame.mixer.Sound("assets/audio/menu/button_click.mp3")
pygame.mixer.music.play(-1)

# Load and scale images
background = pygame.image.load("graphics/menu/background.png").convert_alpha()
start_img = pygame.image.load("graphics/menu/start.png").convert_alpha()
settings_img = pygame.image.load("graphics/menu/settings.png").convert_alpha()
exit_img = pygame.image.load("graphics/menu/exit.png").convert_alpha()
start_img = pygame.transform.scale(start_img, (start_img.get_width() * 1/5, start_img.get_height() * 1/5))
settings_img = pygame.transform.scale(settings_img, (settings_img.get_width() * 1/5, settings_img.get_height() * 1/5))
exit_img = pygame.transform.scale(exit_img, (exit_img.get_width() * 1/6, exit_img.get_height() * 1/6))
hall_of_fame_img = pygame.image.load("graphics/menu/hallOfFameButton.png").convert_alpha()

# Render text
text_title = title_font.render("Miners' Bastion", True, 'yellow')

# Animation variables
background_y = 800
moving_up = True

def back_to_main_menu():
    global current_state
    current_state = 'MAIN_MENU'
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def set_current_state(state):
    global current_state
    current_state = state

startButton = Button(SCREEN_WIDTH / 2 - start_img.get_width() / 2, 300, start_img, action=lambda: set_current_state('LEVEL_SELECTION'))
settingsButton = Button(SCREEN_WIDTH - settings_img.get_width() - 10, 10, settings_img, action=lambda: set_current_state('SETTINGS'))
hall_of_fame_button = Button(SCREEN_WIDTH / 2 - hall_of_fame_img.get_width() / 2, 700, hall_of_fame_img, action=lambda: set_current_state('HALL_OF_FAME'))
exitButton = Button(SCREEN_WIDTH / 2 - exit_img.get_width() / 2, 450, exit_img, action=lambda: pygame.quit())

current_state = 'MAIN_MENU'

# Main loop
while True:
    dt = pygame.time.Clock().tick(60) / 1000

    settings = load_settings()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                startButton.is_clicked()
                settingsButton.is_clicked()
                hall_of_fame_button.is_clicked()
                exitButton.is_clicked()
    screen.blit(background, (0, 0))
    screen.blit(text_title, (SCREEN_WIDTH / 2 - text_title.get_width() / 2, background_y))

    startButton.draw(screen)
    settingsButton.draw(screen)
    hall_of_fame_button.draw(screen)
    exitButton.draw(screen)

    # Title animation
    if moving_up:
        background_y -= 60 * dt
        if background_y <= 800:
            moving_up = False
    else:
        background_y += 60 * dt
        if background_y >= 850:
            moving_up = True

    pygame.display.update()

    # Handle state transitions
    if current_state == 'SETTINGS':
        settingsPanel(back_to_main_menu)
    
    if current_state == 'LEVEL_SELECTION':
        levelSelection(back_to_main_menu)

    if current_state == 'MAIN_MENU':
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)

    if current_state == 'HALL_OF_FAME':
        hallOfFame(back_to_main_menu)

main()