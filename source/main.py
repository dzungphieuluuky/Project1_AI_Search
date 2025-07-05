from button import *
from sound import *
from game import Game
from map import *
from font import *


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

DELAY_TIME = 1000

# DO NOT TOUCH! 
pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

GRID_SIZE = 80
GRID_ORIGIN = (300, 90)
ASSETS_PATH = "./assets"

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
    algo_names = ["Breadth-First Search", "Depth-First Search",
                  "Uniform-Cost Search", "A* Search"]
    
    is_solved = False
    buttons = []
    selected_algo_index = 0
    selected_map_index = 0
    step_count = 0
    total_cost = 0
    pause = True
    last_render_time = 0
    game = Game(maps[selected_map_index], screen, GRID_SIZE, GRID_ORIGIN, ASSETS_PATH)
    def change_algo() -> None:
        nonlocal pause
        if not pause:
            return
        nonlocal selected_algo_index
        nonlocal selected_algo_button
        nonlocal is_solved
        is_solved = False
        total_cost = 0
        step_count = 0
        total_cost_button.set_text(f'Total cost: {total_cost}')
        step_count_button.set_text(f'Step count: {step_count}')
        selected_algo_index = (selected_algo_index + 1) % len(algo_names)
        selected_algo_button.set_text(algo_names[selected_algo_index])

    selected_algo_name = button_font.render('Breadth-First Search', True, BLACK)
    selected_algo_button = Button('Breadth-First Search', 20, 20,
                                  selected_algo_name.get_width() + 35, selected_algo_name.get_height() + 35, 
                                  FRENCH_BLUE, change_algo)
    buttons.append(selected_algo_button)

    step_count_text_surf = button_font.render('Step count: 0', True, BLACK)
    step_count_button = Button(f'Step count: {step_count}', 20, 20 + selected_algo_name.get_height() + 40,
                               step_count_text_surf.get_width() + 35, step_count_text_surf.get_height() + 35,
                               AMARANTH_PURPLE, lambda: None, expandable=False)
    buttons.append(step_count_button)

    total_cost_text_surf = button_font.render('Total cost: 0', True, BLACK)
    total_cost_button = Button(f'Total cost: {total_cost}', 20, 20 + 2 * (selected_algo_name.get_height() + 40),
                               total_cost_text_surf.get_width() + 35, total_cost_text_surf.get_height() + 35,
                               ZOMP, lambda: None, expandable=False)
    buttons.append(total_cost_button)

    reset_surf = button_font.render('Reset (R)', True, BLACK)
    reset_button_y_position = HEIGHT - 60 - reset_surf.get_height()
    reset_button = Button('Reset (R)', 20, reset_button_y_position,
                          reset_surf.get_width() + 35, reset_surf.get_height() + 35,
                          AMARANTH_PURPLE, start_game)
    buttons.append(reset_button)

    quit_image = pygame.image.load('./assets/quit_button.png').convert_alpha()
    quit_image = pygame.transform.scale_by(quit_image, 0.12)
    quit_button = Button(quit_image, WIDTH - 20 - quit_image.get_width(), 20,
                         quit_image.get_width(), quit_image.get_height(),
                         None, quit_game)
    buttons.append(quit_button)

    def change_play_pause():
        nonlocal pause
        pause = not pause
        pause_play_button.set_text('Play (P)' if pause else 'Pause (P)')
        print(f'Pause: {pause}') # for debug

    pause_play_surf = button_font.render('Play (P)', True, BLACK)
    pause_play_button = Button('Play (P)', 20, reset_button_y_position - (pause_play_surf.get_height() + 40),
                          pause_play_surf.get_width() + 35, pause_play_surf.get_height() + 35,
                          ZOMP, change_play_pause)
    buttons.append(pause_play_button)

    def change_map():
        nonlocal pause
        if not pause:
            return
        nonlocal selected_map_index
        nonlocal is_solved
        total_cost = 0
        step_count = 0
        is_solved = False
        selected_map_index = (selected_map_index + 1) % 11
        total_cost_button.set_text(f'Total cost: {total_cost}')
        step_count_button.set_text(f'Step count: {step_count}')
        map_select_button.set_text(f'Map: {selected_map_index}')

    map_select_surf = button_font.render('Map: 0', True, BLACK)
    map_select_button = Button(f'Map: 0', 20, reset_button_y_position - 2 * (pause_play_surf.get_height() + 40),
                               map_select_surf.get_width() + 35, map_select_surf.get_height() + 35,
                               FRENCH_BLUE, change_map)
    buttons.append(map_select_button)

    running = True
    while running:
        screen.fill(ATOMIC_TANGERINE)
        
        for button in buttons:
            button.draw_button(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit_game()
            
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

        current_time = pygame.time.get_ticks()

        if not pause:
            if not is_solved:
                game = Game(maps[selected_map_index], screen, GRID_SIZE, GRID_ORIGIN, ASSETS_PATH)
                total_cost = 0
                step_count = 0
                solution, search_time, memory_usage, expanded_nodes = game.algos[selected_algo_index]()
                is_solved = True
                print(f"Map: {selected_map_index}, Algorithm: {algo_names[selected_algo_index]}")
                if len(solution) == 0:
                    print(f"No solution found!")
                else:
                    print(f"Solution: {solution}, Search time: {search_time}, Memory usage: {memory_usage}, Expanded nodes: {expanded_nodes}")
                    print(f"Total cost: {solution[-1]['total_cost']}, Step counts: {len(solution) - 1}")

            if current_time - last_render_time >= DELAY_TIME and step_count < len(solution):
                total_cost_button.set_text(f"Total cost: {solution[step_count]['total_cost']}")
                step_count_button.set_text(f"Step count: {step_count}")
                for car_id, position in solution[step_count]['state'].items():
                    game.vehicles[car_id].col, game.vehicles[car_id].row = position
                step_count += 1
                last_render_time = current_time
            
            if step_count > 0 and step_count == len(solution):
                congrats_screen(selected_map_index, algo_names[selected_algo_index],
                                step_count, total_cost, is_solved)
            
            # add render function here
        game.draw_all_sprites()
        pygame.display.flip()
        clock.tick(FPS)


def introduction_screen() -> None:
    introductions = [
        "This app helps you visualize AI search algorithms via Rush Hour Game.",
        "Here are some instruction to help you through the game!",
        "1. Use arrow (up/down/left/right) or WASD keys to navigate the game.",
        "2. Change algorithm (DFS/BFS/UCS/A*) by clicking on the algorithm button.",
        "3. The game ends when the target vehicle meets any of 2 conditions:",
        "   <> Successfully exit the map.",
        "   <> Get stuck infinitely in the map.",
        "4. Click the Start Game below to start the search!"
    ]
    # list to hold all buttons
    buttons = []

    title = title_font.render("Introduction", True, BLACK)

    back_button_title = button_font.render("Back to Menu", True, BLACK)
    back_button_width = back_button_title.get_width() + 35
    back_button_height = back_button_title.get_height() + 35
    back_button = Button("Back to Menu", WIDTH - 20 - back_button_width, 20, 
                            back_button_width, back_button_height, ATOMIC_TANGERINE, menu_loop)
    buttons.append(back_button)

    start_button_title = button_font.render("Start Game", True, BLACK)
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

def congrats_screen(map_num: int, algo: str, step_count: int, cost: int, is_solved: bool) -> None:
    buttons = []

    top = HEIGHT // 8
    left = WIDTH // 8
    width = WIDTH // 1.5
    height = HEIGHT // 1.5
    box_rect = pygame.Rect(left, top, width, height)

    # Render text
    lines = [
        "Congratulations!",
        f"Map {map_num} has been",
        f"solved with {algo}!",
        f"Step count: {step_count}",
        f"Total cost: {cost}"
    ]
    reset_surf = button_font.render('Reset (R)', True, BLACK)
    reset_button_x_position = left + 40
    reset_button_y_position = top + height - 40 - reset_surf.get_height()
    reset_button = Button('Reset (R)', reset_button_x_position, reset_button_y_position,
                          reset_surf.get_width() + 35, reset_surf.get_height() + 35,
                          FRENCH_BLUE, start_game)
    buttons.append(reset_button)

    quit_surf = button_font.render('Quit (Q)', True, BLACK)
    quit_button_x_position = left + width - 40 - quit_surf.get_width()
    quit_button = Button('Quit (Q)', quit_button_x_position, reset_button_y_position,
                         quit_surf.get_width() + 35, quit_surf.get_height() + 35,
                         AMARANTH_PURPLE, quit_game)
    buttons.append(quit_button)

    def replay():
        nonlocal running
        nonlocal is_solved
        is_solved = False
        running = False

    replay_surf = button_font.render('RePlay (P)', True, BLACK)
    replay_button_x_position = (reset_button_x_position + reset_surf.get_width() + quit_button_x_position) // 2 - (replay_surf.get_width() // 2)
    replay_button = Button('RePlay (P)', replay_button_x_position, reset_button_y_position,
                           replay_surf.get_width() + 35, replay_surf.get_height() + 35,
                           ZOMP, replay)
    buttons.append(replay_button)


    running = True
    while running:
        screen.fill(CREAM)
        
        pygame.draw.rect(screen, WHITE, box_rect, border_radius=40)
        pygame.draw.rect(screen, BLACK, box_rect, 2, border_radius=40)
        for i, line in enumerate(lines):
            text_surf = title_font.render(line, True, BLACK)
            text_rect = text_surf.get_rect(center=(WIDTH//2, 160 + i * 40))
            screen.blit(text_surf, text_rect)

        # Draw buttons
        for button in buttons:
            button.draw_button(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    reset_button.callback()
                elif event.key == pygame.K_p:
                    replay_button.callback()
                elif event.key == pygame.K_q:
                    quit_button.callback()

            for button in buttons:
                button.handle_event(event)

        pygame.display.flip()
        clock.tick(60)

def quit_game():
    pygame.quit()
    sys.exit()

def main():
    # set loops = -1 to play forever
    # background_music.play(loops=-1)
    menu_loop()

if __name__ == "__main__":
    main()


