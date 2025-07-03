import heapq
import pygame
from timeit import default_timer
import tracemalloc

class Game():
    """
    Car map: the initial state and information of each car on the map
    Example of car map:
    {
        'X': {'orientation': 'H', 'cost': 2, 'position': (2, 0)}
        'Y': {'orientation': 'V', 'cost': 3, 'position': (3, 0)}
    }
    H: horizontal
    V: vertical

    State: the current position of all cars on the map
    Example of the state:
    {
        'X': (4, 5)
        'Y': (6, 7)
    }
    The first is j position (col), the second is i position (row).
    """
    def __init__(self, cars_map: dict) -> None:
        self.exit_row = 2
        self.size = 6
        self.cars_map = cars_map
        self.initial_state = self.get_state_from_map()
        self.algos = [self.bfs_solver, self.dfs_solver, self.ucs_solver, self.a_star_solver]

    def get_state_from_map(self):
        state = {}
        for car, info in self.cars_map.items():
            state[car] = info['position']
        return state
    
    def hash_state(self, state):
        hash_state = tuple(sorted((id, pos) for id, pos in state.items()))
        return hash_state
    
    def is_goal(self, state: dict) -> bool:
        position_player = state['player']
        return position_player[0] + self.cars_map['player']['cost'] - 1 == self.size - 1
    
    def is_free(self, state: dict, row: int, col: int) -> bool:
        # if the cell is out of bound
        if not (0 <= row <= self.size - 1 and 0 <= col <= self.size - 1):
            return False
        
        for car, info in self.cars_map.items():
            orientation = info['orientation']
            length = info['cost']
            col_position, row_position = state[car]
            if orientation == 'H':
                # if the cell collide with horizontal car
                for k in range(length):
                    if (row, col) == (row_position, col_position + k):
                        return False
            else:
                # if the cell collide with vertical car
                for k in range(length):
                    if (row, col) == (row_position + k, col_position):
                        return False
        return True
    
    # nap code Thinh Bui vao day
    def draw_all_sprites(self) -> None:
        pass

    def get_successors(self, state: dict) -> list[tuple[dict, int]]:
        # list of next posisble states and cost
        results = []

        for car, info in self.cars_map.items():
            col, row = state[car]
            orientation = info['orientation']
            cost = info['cost']

            # horizontal car
            if orientation == 'H':
                # check to move right
                if self.is_free(state, row, col + cost):
                    next_state = state.copy()
                    new_col = col + 1
                    next_state[car] = (new_col, row)
                    results.append((next_state, cost))
                # check to move left
                if self.is_free(state, row, col - 1):
                    next_state = state.copy()
                    new_col = col - 1
                    next_state[car] = (new_col, row)
                    results.append((next_state, cost))    
            # vertical car
            else:
                # check to move down
                if self.is_free(state, row + cost, col):
                    next_state = state.copy()
                    new_row = row + 1
                    next_state[car] = (col, new_row)
                    results.append((next_state, cost))
                # check to move up
                if self.is_free(state, row - 1, col):
                    next_state = state.copy()
                    new_row = row - 1
                    next_state[car] = (col, new_row)
                    results.append((next_state, cost))
        return results
    
    def ucs_solver(self) -> tuple[list, int, int, int]:
        ''' 
        Solution is a list of dictionaries each contains: state, total cost
        Example of a solution:
        solution = [
        {'state': some state, 'cost': some cost},
        {'state': another state, 'cost': another cost}]
        '''
        solution = []

        # metrics to measure performance
        search_time = 0
        memory_usage = 0
        expanded_nodes = 0
        
        # begin timer
        start = default_timer()

        tracemalloc.start()
        state = self.initial_state
        frontier = []
        parent_of = {}
        expanded = set()
        # hash the state into a tuple to make it be able to used as a key
        cost_of = {self.hash_state(state): 0}

        # counter used as a secondary comparison when cost is equal
        # make sure to select following FIFO order
        counter = 0
        heapq.heappush(frontier, (0, counter, state))
        counter += 1

        while frontier:
            current_cost, _, current_state = heapq.heappop(frontier)
            
            hashed_current_state = self.hash_state(current_state)
            if hashed_current_state not in expanded:
                expanded.add(hashed_current_state)
            else:
                continue
            
            if self.is_goal(current_state):
                expanded_nodes = len(expanded)
                end = default_timer()
                search_time = end - start
                this_state = current_state
                while self.hash_state(this_state) in parent_of:
                    this_cost = cost_of[self.hash_state(this_state)]
                    solution.append({'total_cost' : this_cost, 'state' : this_state})
                    this_state = parent_of[self.hash_state(this_state)]
                
                # add the initial state
                solution.append({'total_cost' : 0, 'state': self.initial_state})
                
                # reverse the list to get the right order of state
                solution = list(reversed(solution))
                memory_size, memory_peak = tracemalloc.get_traced_memory()
                tracemalloc.reset_peak()
                memory_usage = memory_peak
                return solution, search_time, memory_usage, expanded_nodes
            
            for next_state, next_cost in self.get_successors(current_state):
                new_cost = current_cost + next_cost
                hashed_next_state = self.hash_state(next_state)
                if hashed_next_state not in cost_of or cost_of[hashed_next_state] > new_cost:
                    cost_of[hashed_next_state] = new_cost
                    heapq.heappush(frontier, (new_cost, counter, next_state))
                    counter += 1
                    parent_of[hashed_next_state] = current_state
        
        print("No solution is found!")
        search_time = default_timer() - start
        memory_size, memory_peak = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()
        memory_usage = memory_peak
        expanded_nodes = len(expanded)
        return (solution, search_time, memory_usage, expanded_nodes)
    
    def bfs_solver(self):
        # dummy placeholder
        return ([], 0, 0, 0)
        # YOUR CODE HERE

    def dfs_solver(self):
        # dummy placeholder
        return ([], 0, 0, 0)
        # YOUR CODE HERE

    def a_star_solver(self):
        # dummy placeholder
        return ([], 0, 0, 0)
        # YOUR CODE HERE