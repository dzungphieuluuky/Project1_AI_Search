from menu import Button, font, small_font
import pygame
import sys

WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
DARK_BLUE = (0, 80, 200)
BLACK = (0, 0, 0)

AMARANTH_PURPLE = (170, 17, 85)
ATOMIC_TANGERINE = (247, 157, 101)
FRENCH_BLUE = (0, 114, 187)
CREAM = (239, 242, 192)
ZOMP = (81, 158, 138)

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

    buttons = [Button("Play", button_x_coordinate, last_button_y_coordinate - 2 * (button_height + 10), 
                      button_width, button_height, ATOMIC_TANGERINE, start_game),
               Button("Introduction", button_x_coordinate, last_button_y_coordinate - (button_height + 10), 
                      button_width, button_height, ZOMP, introduction_screen),
               Button("Quit Game", button_x_coordinate, last_button_y_coordinate, 
                      button_width, button_height, AMARANTH_PURPLE, pygame.quit)]
    
    hovered_button = 0
    while running:
        screen.blit(image, image_rect)
        title = font.render("Rush Hour with AI", True, AMARANTH_PURPLE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        
        for button in buttons:
            button.draw_button(screen)

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

def introduction_screen():
    running = True
    title_font = pygame.font.SysFont("Comic Sans MS", 60, bold=True)
    body_font = pygame.font.SysFont("Arial", 28)

    while running:
        screen.fill(CREAM)

        title = title_font.render("Introduction", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        introductions = [
            "This app helps you visualize AI search algorithms via Rush Hour Game.",
            "Buttons are floating around to help you navigate better.",
            "Here are some instruction to help you through the game!",
            "1. Use arrow keys (up/down/left/right) or WASD keys to navigate the game.",
            "2. Select search algorithm (DFS/BFS/UCS/A*) to find a solution.",
            "3. The game ends when the target vehicle satisfies any of 2 conditions:",
            "   <> Successfully exit the map.",
            "   <> Get stuck infinitely in the map.",
            "4. Click the Start Game below to start the search!"
        ]

        for i, line in enumerate(introductions):
            text = small_font.render(line, True, BLACK)
            screen.blit(text, (20, 150 + 40 * i))
        
        back_button_title = body_font.render("Back to Menu", True, BLACK)
        back_button_width = back_button_title.get_width() + 20
        back_button_height = back_button_title.get_height() + 20
        back_button = Button("Back to Menu", WIDTH - 20 - back_button_width, 
                            20, back_button_width, back_button_height, ATOMIC_TANGERINE, menu_loop)

        start_button_title = body_font.render("Start Game", True, BLACK)
        start_button_width = start_button_title.get_width() + 20
        start_button_height = start_button_title.get_height() + 20
        start_button = Button("Start Game", WIDTH // 2 - start_button_width // 2,HEIGHT - 20 - start_button_height, 
                              start_button_width, start_button_height, AMARANTH_PURPLE, start_game)

        # list to hold all buttons
        buttons = [back_button, start_button]
        for button in buttons:
            button.draw_button(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                return
            
            for button in buttons:
                button.handle_event(event=event)
    
        pygame.display.flip()
        clock.tick(FPS)


def main():
    menu_loop()

if __name__ == "__main__":
    main()


