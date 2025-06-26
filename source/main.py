from menu import Button, font, small_font
import pygame
import sys

WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
DARK_BLUE = (0, 80, 200)
BLACK = (0, 0, 0)

pygame.init()
WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Search Visualizer via Rush Hour")
clock = pygame.time.Clock()

def menu_loop():
    running = True
    image = pygame.image.load('./img/background2.jpg').convert_alpha()
    image_rect = image.get_rect()
    button_width = 200
    button_height = 60
    button_x_coordinate = WIDTH // 2 - button_width // 2
    last_button_y_coordinate = HEIGHT - 20 - button_height
    buttons = [Button("Play", button_x_coordinate, last_button_y_coordinate - 2 * (button_height + 10), button_width, button_height, start_game),
               Button("Instructions", button_x_coordinate, last_button_y_coordinate - (button_height + 10), button_width, button_height, instructions),
               Button("Quit Game", button_x_coordinate, last_button_y_coordinate, button_width, button_height, pygame.quit)]
    hovered_button = 0
    while running:
        screen.blit(image, image_rect)
        title = font.render("Rush Hour Visualizer", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        
        for button in buttons:
            button.draw_rect(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    buttons[hovered_button].is_hovered = False
                    hovered_button = (hovered_button - 1) % len(buttons)
                    buttons[hovered_button].is_hovered = True
                
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    buttons[hovered_button].is_hovered = False
                    hovered_button = (hovered_button + 1) % len(buttons)
                    buttons[hovered_button].is_hovered = True
                
                elif event.key == pygame.K_ESCAPE:
                    running = False

            for button in buttons:
                button.handle_event(event=event)
        
        
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


