import pygame

pygame.init()
background_music = pygame.mixer.Sound('./assets/game-background.mp3')
background_music.set_volume(0.4)
hover_sound = pygame.mixer.Sound('./assets/click.mp3')
click_sound = pygame.mixer.Sound('./assets/mouse-click.mp3')
