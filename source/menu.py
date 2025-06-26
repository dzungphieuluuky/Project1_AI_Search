import pygame

WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
DARK_BLUE = (0, 80, 200)
BLACK = (0, 0, 0)

pygame.font.init()
font = pygame.font.SysFont("Cascadia Mono", 48)
small_font = pygame.font.SysFont("Cascadia Mono", 32)

class Button:
    # initialize button class with callback function
    def __init__(self, text, x, y, w, h, callback):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

        # callback function to call the function of the button
        self.normal_color = BLUE
        self.hovered_color = DARK_BLUE
        self.callback = callback
        self.hover = False

    def draw_rect(self, surface):
        color = self.hovered_color if self.hover else self.normal_color
        pygame.draw.rect(surface, color, self.rect)
        text_surf = small_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.hover:
            self.callback()