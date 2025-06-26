import pygame

WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
DARK_BLUE = (0, 80, 200)
BLACK = (0, 0, 0)

pygame.init()
font = pygame.font.SysFont("Cascadia Mono", 96)
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
        self.is_hovered = False
        self.text_surface = None

    def draw_rect(self, surface):
        self.surface = surface
        color = self.hovered_color if self.is_hovered else self.normal_color
        pygame.draw.rect(surface, color, self.rect)
        text_surf = small_font.render(self.text, True, WHITE)
        self.text_surface = text_surf
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        if self.is_hovered:
            pygame.transform.smoothscale_by(text_surf, 1.1)


    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif self.is_hovered and (event.type == pygame.MOUSEBUTTONDOWN or
                                  event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or
                                                                    event.key == pygame.K_SPACE)):
            self.callback()