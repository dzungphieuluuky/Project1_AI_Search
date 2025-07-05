import pygame
from typing import Union
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
DARK_BLUE = (0, 80, 200)
BLACK = (0, 0, 0)

pygame.init()
hover_sound = pygame.mixer.Sound('./assets/click.mp3')
click_sound = pygame.mixer.Sound('./assets/mouse-click.mp3')
font = pygame.font.SysFont("Roboto", 96, bold=True)
small_font = pygame.font.SysFont("Cascadia Mono", 32)

class Button:
    # initialize button class with callback function
    def __init__(self, text : Union[str, pygame.Surface], x: float, y: float, width: float, height: float, color: tuple[int, int, int], callback: callable, expandable = True) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        # callback function to call the function of the button
        self.callback = callback
        self.expandable = expandable
        self.last_hovered = False
        self.is_hovered = False

    def draw_button(self, surface: pygame.surface) -> None:
        if isinstance(self.text, pygame.Surface):
            text_surf = self.text
            if self.is_hovered and self.expandable:
                text_surf = pygame.transform.scale_by(text_surf, 1.1)
                if self.last_hovered == False:
                    hover_sound.play()
            self.last_hovered = self.is_hovered
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)
        else:
            text_surf = small_font.render(self.text, True, WHITE)
            if self.is_hovered and self.expandable:
                text_surf = pygame.transform.scale_by(text_surf, 1.1)
                pygame.draw.rect(surface, self.color, self.rect.scale_by(1.1, 1.1), border_radius=15)
                if self.last_hovered == False:
                    hover_sound.play()
            else:
                pygame.draw.rect(surface, self.color, self.rect, border_radius=15)
            self.last_hovered = self.is_hovered
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def handle_event(self, event: pygame.event) -> None:
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif self.is_hovered and (event.type == pygame.MOUSEBUTTONDOWN or
                                  event.type == pygame.KEYDOWN and event.key in [pygame.K_RETURN, pygame.K_SPACE]):
            if self.expandable:
                click_sound.play()
            self.callback()
    
    def set_text(self, text) -> None:
        self.text = text