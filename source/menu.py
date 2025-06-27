import pygame

WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
DARK_BLUE = (0, 80, 200)
BLACK = (0, 0, 0)

pygame.init()
font = pygame.font.SysFont("Montserrat", 96, bold=True)
small_font = pygame.font.SysFont("Russo One", 32)

class Button:
    # initialize button class with callback function
    def __init__(self, text : str, x: float, y: float, width: float, height: float, color: tuple, callback: callable):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.button_rect = None
        # callback function to call the function of the button
        self.callback = callback

        self.is_hovered = False

    def draw_button(self, surface):
        if self.button_rect is None:
            self.button_rect = pygame.draw.rect(surface, self.color, self.rect, border_radius=15)
        else: 
            pygame.draw.rect(surface, self.color, self.rect, border_radius=15)
        text_surf = small_font.render(self.text, True, WHITE)
        if self.is_hovered:
            text_surf = pygame.transform.scale_by(text_surf, 1.1)
            self.button_rect.scale_by_ip(1.1, 1.1)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif self.is_hovered and (event.type == pygame.MOUSEBUTTONDOWN or
                                  event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or
                                                                    event.key == pygame.K_SPACE)):
            self.callback()