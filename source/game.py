import heapq
import pygame
class Game():
    """
    Car map: the initial state and information of each car on the map
    Example of car map:
    {
        'X': {'orientation': 'H', 'length': 2, 'cost': 2, 'position': (2, 0)}
        'Y': {'orientation': 'V', 'length': 3, 'cost': 3, 'position': (3, 0)}
    }
    H: horizontal
    V: vertical

    State: the current position of all cars on the map
    Example of the state:
    {
        'X': (4, 5)
        'Y': (6, 7)
    }
    The first is i position, the second is j position
    """
    def __init__(self, initial_state, exit_row, cars_map, size):
        self.initial_state = initial_state
        self.exit_row = exit_row
        self.size = size
        self.cars_map = cars_map
    
    def is_goal(self, state):
        player_car = state['player']
        return player_car[1] + self.cars_map['player']['length'] - 1 == self.size - 1
    
    def is_free(self, state, row, col):
        if not (0 <= row <= self.size - 1 and 0 <= col <= self.size - 1):
            return False
        for car, info in self.cars_map.items():
            orientation = info['orientation']
            length = info['length']
            i_position, j_position = state[car]
            if orientation == 'H':
                for k in range(length):
                    if (row, col) == (i_position, j_position + k):
                        return False
            else:
                for k in range(length):
                    if (row, col) == (i_position + k, j_position):
                        return False
        return True
    
    # nap code Thinh Bui vao day
    def draw_all_sprites(self):
        pass

    def get_successors(self, state):
        # list of next posisble states and cost
        results = []

        for car, info in self.cars_map.items():
            row, col = state[car]
            orientation = info['orientation']
            cost = info['cost']

            if orientation == 'H':
                if self.is_free(state, row, col + 1):
                    next_state = state
                    new_col = col + 1
                    next_state[car] = (row, new_col)
                    results.append((next_state, cost))
                if self.is_free(state, row, col - 1):
                    next_state = state
                    new_col = col - 1
                    next_state[car] = (row, new_col)
                    results.append((next_state, cost))    
            else:
                if self.is_free(state, row + 1, col):
                    next_state = state
                    new_row = row + 1
                    next_state[car] = (new_row, col)
                    results.append((next_state, cost))
                if self.is_free(state, row - 1, col):
                    next_state = state
                    new_row = row - 1
                    next_state[car] = (new_row, col)
                    results.append((next_state, cost))
        return results
    
    def ucs_solver(self):
        state = self.initial_state
        step_count = 0
        total_cost = None
        frontier = []
        predecessor = {}
        expanded = set()
        cost = {state: 0}
        heapq.heappush(frontier, (0, state))

        while not frontier:
            current_cost, current_state = heapq.heappop(frontier)
            total_cost = current_cost
            
            if current_state not in expanded:
                expanded.add(current_state)
                step_count += 1
            else:
                continue
            
            if self.is_goal(current_state):
                return
            
            for next_state, next_cost in self.get_successors(current_state):
                new_cost = current_cost + next_cost
                if next_state not in cost or cost[next_state] > new_cost:
                    cost[next_state] = new_cost
                    heapq.heappush(frontier, (new_cost, next_state))
                    predecessor[next_state] = current_state