import pygame
import os
class Vehicle:
    def __init__(self, id: str, col: int, row: int, length: int, orientation: str) -> None:
        self.id = id 
        self.col = col  
        self.row = row                               
        self.length = length       
        self.orientation = orientation

    def get_id(self) -> str:
        return self.id
    
    def get_position(self) -> tuple[int, int]:
        return self.row, self.col
    
    def get_length(self) -> int:
        return self.length
    
    def get_orientation(self) -> str:
        return self.orientation
    
    def move(self, delta) -> None:
        if self.orientation == 'H':
            self.col += delta
        else:
            self.row += delta

    def get_occupied_cells(self) -> list[tuple[int, int]]:
        cells = []
        for i in range(self.length):
            if self.orientation == 'H':
                cells.append((self.col + i, self.row))
            else:
                cells.append((self.col, self.row + i))
        return cells
    
class Car(Vehicle):
    def __init__(self, id: str, col: int, row: int, orientation: str) -> None:
        super().__init__(id, col, row, 2, orientation)

    def draw(self, folder_path: str, grid_size: int) -> pygame.Surface:
        if self.id == "player":
            filename = "player.png"
            width = grid_size * 2
            height = grid_size
        elif self.orientation == 'H':
            filename = "horizontal_car.png"
            width = grid_size * 2
            height = grid_size
        else:
            filename = "vertical_car.png"
            width = grid_size
            height = grid_size * 2
        image_path = os.path.join(folder_path, filename)
        image = pygame.image.load(image_path).convert_alpha()
        return pygame.transform.scale(image, (width, height))
    
class Truck(Vehicle):
    def __init__(self, id: str, col: int, row: int, orientation: str) -> None:
        super().__init__(id, col, row, 3, orientation)

    def draw(self, folder_path: str, grid_size: int) -> pygame.Surface:
        if self.orientation == 'H':
            filename = "horizontal_truck.png"
            width = grid_size * 3
            height = grid_size
        else:
            filename = "vertical_truck.png"
            width = grid_size
            height = grid_size * 3
        image_path = os.path.join(folder_path, filename)
        image = pygame.image.load(image_path).convert_alpha()
        return pygame.transform.scale(image, (width, height))