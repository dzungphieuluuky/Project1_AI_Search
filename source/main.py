from menu import Button, font, small_font
import pygame
import sys

WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
DARK_BLUE = (0, 80, 200)
BLACK = (0, 0, 0)

pygame.init()
WIDTH = 600
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Search Visualizer via Rush Hour")
clock = pygame.time.Clock()

def menu_loop():
    running = True
    image = pygame.image.load('./img/background.jpg').convert_alpha()
    image_rect = image.get_rect()
    button_width = 200
    button_height = 60
    button_x_coordinate = WIDTH // 2 - button_width // 2
    buttons = [Button("Play", button_x_coordinate, 220, button_width, button_height, start_game),
               Button("Instructions", button_x_coordinate, 290, button_width, button_height, instructions),
               Button("Quit Game", button_x_coordinate, 360, button_width, button_height, pygame.quit)]
    while running:
        screen.blit(image, image_rect)
        title = font.render("Main Menu", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False

            for button in buttons:
                button.handle_event(event=event)
        
        for button in buttons:
            button.draw_rect(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

def start_game():
    pass

def instructions():
    pass


def main():
    menu_loop()

if __name__ == "__main__":
    main()


