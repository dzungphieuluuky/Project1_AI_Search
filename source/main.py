from menu import Button, font, small_font
from game import Game
import pygame
import sys

# Color macro
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
DARK_BLUE = (0, 80, 200)
BLACK = (0, 0, 0)

AMARANTH_PURPLE = (170, 17, 85)
ATOMIC_TANGERINE = (247, 157, 101)
FRENCH_BLUE = (0, 114, 187)
CREAM = (239, 242, 192)
ZOMP = (81, 158, 138)

# super important line
pygame.init()
# init background music
background_music = pygame.mixer.Sound('./assets/game-background.mp3')

WIDTH = 800
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rush Hour AI Search Visualizer")
clock = pygame.time.Clock()

def menu_loop() -> None:
    running = True
    image = pygame.image.load('./assets/background2.jpg').convert_alpha()
    image_rect = image.get_rect()

    button_width = 200
    button_height = 60
    button_x_coordinate = WIDTH // 2 - button_width // 2
    last_button_y_coordinate = HEIGHT - 20 - button_height

    buttons = [Button("Start Game", button_x_coordinate, last_button_y_coordinate - 2 * (button_height + 10), 
                      button_width, button_height, ATOMIC_TANGERINE, start_game),
               Button("Introduction", button_x_coordinate, last_button_y_coordinate - (button_height + 10), 
                      button_width, button_height, ZOMP, introduction_screen),
               Button("Quit Game", button_x_coordinate, last_button_y_coordinate, 
                      button_width, button_height, AMARANTH_PURPLE, pygame.quit)]
    
    hovered_button = 0
    title = font.render("Rush Hour with AI", True, AMARANTH_PURPLE)

    while running:
        screen.blit(image, image_rect)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        
        for button in buttons:
            button.draw_button(screen)

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False
            
            elif event.type == pygame.KEYDOWN:
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

def start_game() -> None:
    body_font = pygame.font.SysFont("Consolas", 24)

    algo_names = ["Breadth-First Search", "Depth-First Search",
                  "Uniform-Cost Search", "A* Search"]
    
    # algo_function = [game.bfs_solver, game.dfs_solver,
    #                  game.ucs_solver, game.a_star_solver]
    
    buttons = []
    selected_algo_index = 0
    step_count = 0
    total_cost = 0
    pause = False

    def change_algo() -> None:
        nonlocal selected_algo_index
        nonlocal selected_algo_button
        selected_algo_index = (selected_algo_index + 1) % len(algo_names)
        selected_algo_button.set_text(algo_names[selected_algo_index])

    selected_algo_name = body_font.render('Breadth-First Search', True, BLACK)
    selected_algo_button = Button('Breadth-First Search', 20, 20,
                                  selected_algo_name.get_width() + 35, selected_algo_name.get_height() + 35, 
                                  FRENCH_BLUE, change_algo)
    buttons.append(selected_algo_button)

    step_count_text_surf = body_font.render('Step count: 0', True, BLACK)
    step_count_button = Button(f'Step count: {step_count}', 20, 20 + selected_algo_name.get_height() + 40,
                               step_count_text_surf.get_width() + 35, step_count_text_surf.get_height() + 35,
                               AMARANTH_PURPLE, lambda: None, expandable=False)
    buttons.append(step_count_button)

    total_cost_text_surf = body_font.render('Total cost: 0', True, BLACK)
    total_cost_button = Button(f'Total cost: {total_cost}', 20, 20 + 2 * (selected_algo_name.get_height() + 40),
                               total_cost_text_surf.get_width() + 35, total_cost_text_surf.get_height() + 35,
                               ZOMP, lambda: None, expandable=False)
    buttons.append(total_cost_button)

    reset_surf = body_font.render('Reset (R)', True, BLACK)
    reset_button_y_position = HEIGHT - 60 - reset_surf.get_height()
    reset_button = Button('Reset (R)', 20, reset_button_y_position,
                          reset_surf.get_width() + 35, reset_surf.get_height() + 35,
                          AMARANTH_PURPLE, start_game)
    buttons.append(reset_button)

    def change_play_pause():
        nonlocal pause
        pause = not pause
        pause_play_button.set_text('Play (P)' if pause else 'Pause (P)')
        print(f'Pause: {pause}') # for debug

    pause_play_surf = body_font.render('Pause (P)', True, BLACK)
    pause_play_button = Button('Pause (P)', 20, reset_button_y_position - (pause_play_surf.get_height() + 40),
                          pause_play_surf.get_width() + 35, pause_play_surf.get_height() + 35,
                          ZOMP, change_play_pause)
    buttons.append(pause_play_button)

    running = True
    while running:
        screen.fill(ATOMIC_TANGERINE)

        for button in buttons:
            button.draw_button(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    pause_play_button.callback()
                elif event.key == pygame.K_r:
                    reset_button.callback()
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    selected_algo_index = (selected_algo_index + 1) % len(algo_names)
                    selected_algo_button.set_text(algo_names[selected_algo_index])
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    selected_algo_index = (selected_algo_index - 1) % len(algo_names)
                    selected_algo_button.set_text(algo_names[selected_algo_index])

            for button in buttons:
                button.handle_event(event=event)
        
        pygame.display.flip()
        clock.tick(FPS)


def introduction_screen() -> None:
    title_font = pygame.font.SysFont("Consolas", 60, bold=True)
    body_font = pygame.font.SysFont("Cascadia Mono", 28)
    intro_font = pygame.font.SysFont("Consolas", 20)

    introductions = [
        "This app helps you visualize AI search algorithms via Rush Hour Game.",
        "Here are some instruction to help you through the game!",
        "1. Use arrow (up/down/left/right) or WASD keys to navigate the game.",
        "2. Select search algorithm (DFS/BFS/UCS/A*) by clicking on the algorithm button.",
        "3. The game ends when the target vehicle satisfies any of 2 conditions:",
        "   <> Successfully exit the map.",
        "   <> Get stuck infinitely in the map.",
        "4. Click the Start Game below to start the search!"
    ]
    # list to hold all buttons
    buttons = []

    title = title_font.render("Introduction", True, BLACK)

    back_button_title = body_font.render("Back to Menu", True, BLACK)
    back_button_width = back_button_title.get_width() + 35
    back_button_height = back_button_title.get_height() + 35
    back_button = Button("Back to Menu", WIDTH - 20 - back_button_width, 20, 
                            back_button_width, back_button_height, ATOMIC_TANGERINE, menu_loop)
    buttons.append(back_button)

    start_button_title = body_font.render("Start Game", True, BLACK)
    start_button_width = start_button_title.get_width() + 35
    start_button_height = start_button_title.get_height() + 35
    start_button = Button("Start Game", WIDTH // 2 - start_button_width // 2,HEIGHT - 20 - start_button_height, 
                            start_button_width, start_button_height, AMARANTH_PURPLE, start_game)
    buttons.append(start_button)

    running = True
    while running:
        screen.fill(CREAM)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 50))

        # rendering intro text
        for i, line in enumerate(introductions):
            text = intro_font.render(line, True, BLACK)
            screen.blit(text, (20, 150 + 40 * i))
        
        for button in buttons:
            button.draw_button(screen)

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            
            for button in buttons:
                button.handle_event(event=event)
    
        pygame.display.flip()
        clock.tick(FPS)


def main():
    # set loops = -1 to play forever
    background_music.play(loops=-1)
    menu_loop()

if __name__ == "__main__":
    main()


