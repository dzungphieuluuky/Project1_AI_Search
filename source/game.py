import heapq
from collections import deque
import pygame
from timeit import default_timer
import tracemalloc
import os
from vehicle import Car, Truck
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
    def __init__(self, cars_map: dict, screen : pygame.Surface, grid_size : int, grid_origin: tuple[int, int], assets_path: str) -> None:
        self.exit_row = 2
        self.size = 6
        self.cars_map = cars_map
        self.initial_state = self.get_state_from_map()
        self.algos = [self.bfs_solver, self.dfs_solver, self.ucs_solver, self.a_star_solver]

        self.grid_size = grid_size
        self.grid_origin = grid_origin
        self.assets_path = assets_path
        self.screen = screen
        self.vehicles = {}
        for id, info in self.cars_map.items():
            col, row = info['position']
            orientation = info['orientation']
            length = info['cost']
            if length == 2:
                self.vehicles[id] = Car(id, col, row, orientation)
            else:
                self.vehicles[id] = Truck(id, col, row, orientation)
        self.background_image = pygame.image.load(os.path.join(self.assets_path, "map.png")).convert()
        self.background_image = pygame.transform.scale(self.background_image,(self.grid_size * self.size, self.grid_size * self.size))

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
    
    def draw_all_sprites(self) -> None:
        x0, y0 = self.grid_origin
        map_width = self.size * self.grid_size
        map_height = self.size * self.grid_size
        self.screen.blit(self.background_image, (x0, y0))
        pygame.draw.rect(self.screen, (0, 102, 0), (x0, y0, map_width, map_height), width = 4)
        exit_rect = pygame.Rect(x0 + self.size * self.grid_size, y0 + self.exit_row * self.grid_size, 20, self.grid_size)
        pygame.draw.rect(self.screen, (204, 102, 0), exit_rect)
        for vehicle in self.vehicles.values():
            image = vehicle.draw(self.assets_path, self.grid_size)
            x = x0 + vehicle.col * self.grid_size
            y = y0 + vehicle.row * self.grid_size
            self.screen.blit(image, (x, y))

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
    
    def ucs_solver(self) -> tuple[list[dict], int, int, int]:
        ''' 
        Solution is a list of dictionaries each contains: state, total cost
        Example of a solution:
        solution = [
        {'state': some state, 'total_cost': some cost},
        {'state': another state, 'total_cost': another cost}]
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
                return (solution, search_time, memory_usage, expanded_nodes)
            
            for next_state, next_cost in self.get_successors(current_state):
                new_cost = current_cost + next_cost
                hashed_next_state = self.hash_state(next_state)
                if hashed_next_state not in cost_of or cost_of[hashed_next_state] > new_cost:
                    cost_of[hashed_next_state] = new_cost
                    heapq.heappush(frontier, (new_cost, counter, next_state))
                    counter += 1
                    parent_of[hashed_next_state] = current_state
        # if no solution
        expanded_nodes = len(expanded)
        end = default_timer()
        search_time = end - start
        memory_size, memory_peak = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()
        memory_usage = memory_peak
        return (solution, search_time, memory_usage, expanded_nodes)
    
    def bfs_solver(self) -> tuple[list[dict], int, int, int]:
        solution = []
        search_time = 0
        memory_usage = 0
        expanded_nodes = 0

        start = default_timer()
        tracemalloc.start()

        state = self.initial_state
        frontier = deque()
        frontier.append(state)
        parent_of = {}
        expanded = set()
        while frontier:
            current_state = frontier.popleft()
            hashed_current_state = self.hash_state(current_state)

            if hashed_current_state in expanded:
                continue
            expanded.add(hashed_current_state)

            if self.is_goal(current_state):
                expanded_nodes = len(expanded)
                end = default_timer()
                search_time = end - start
                this_state = current_state
                path = []
                while self.hash_state(this_state) in parent_of:
                    path.append(this_state)
                    this_state = parent_of[self.hash_state(this_state)]
                path.append(this_state)
                path.reverse()
                solution = [{'total_cost': i, 'state': s} for i, s in enumerate(path)]

                memory_size, memory_peak = tracemalloc.get_traced_memory()
                tracemalloc.reset_peak()
                memory_usage = memory_peak
                return (solution, search_time, memory_usage, expanded_nodes)

            for next_state, _ in self.get_successors(current_state):
                hashed_next_state = self.hash_state(next_state)
                if hashed_next_state not in expanded:
                    frontier.append(next_state)
                    parent_of[hashed_next_state] = current_state

        expanded_nodes = len(expanded)
        end = default_timer()
        search_time = end - start
        memory_size, memory_peak = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()
        memory_usage = memory_peak
        return (solution, search_time, memory_usage, expanded_nodes)

    def dfs_solver(self) -> tuple[list[dict], int, int, int]:
        solution = []
        search_time = 0
        memory_usage = 0
        expanded_nodes = 0

        start = default_timer()
        tracemalloc.start()

        state = self.initial_state
        frontier = [state]

        in_frontier = {self.hash_state(state)} 

        parent_of = {}
        expanded = set()

        while frontier:
            current_state = frontier.pop()
            hashed_current_state = self.hash_state(current_state)
            in_frontier.remove(hashed_current_state)

            if hashed_current_state in expanded:
                continue
            expanded.add(hashed_current_state)

            if self.is_goal(current_state):
                expanded_nodes = len(expanded)
                end = default_timer()
                search_time = end - start

                this_state = current_state
                path = []
                while self.hash_state(this_state) in parent_of:
                    path.append(this_state)
                    this_state = parent_of[self.hash_state(this_state)]
                path.append(this_state)
                path.reverse()
                solution = [{'total_cost': i, 'state': s} for i, s in enumerate(path)]

                memory_size, memory_peak = tracemalloc.get_traced_memory()
                tracemalloc.reset_peak()
                memory_usage = memory_peak
                return solution, search_time, memory_usage, expanded_nodes

            for next_state, _ in reversed(self.get_successors(current_state)):
                hashed_next_state = self.hash_state(next_state)
                if hashed_next_state not in expanded and hashed_next_state not in in_frontier:
                    frontier.append(next_state)
                    in_frontier.add(hashed_next_state)
                    parent_of[hashed_next_state] = current_state
        # if no solution
        expanded_nodes = len(expanded)
        end = default_timer()
        search_time = end - start
        memory_size, memory_peak = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()
        memory_usage = memory_peak
        return (solution, search_time, memory_usage, expanded_nodes)

    def heuristic(self, state: dict) -> int:
        if self.is_goal(state):
            return 0

        goal_car = 'player'
        self.visited = set()
        self.visited.add(goal_car)

        col, _ = state[goal_car]
        len = self.cars_map[goal_car]['cost']

        # k/c còn lại đến đích
        value = len * (self.size - (col + len))
        
        blocker = self.get_blocker(state, goal_car, 'forward', self.size)
        if blocker is not None:
            forward = self.heuristic2(state, blocker, goal_car, direction='forward')
            self.visited = set()
            self.visited.add(goal_car)
            backward = self.heuristic2(state, blocker, goal_car, direction='backward')
            value += min(forward, backward)
        #print("heu: ",value)
        return value
    
    def heuristic2(self, state: dict, car: str, car2: str, direction: str) -> int: 
        #tính chi phí car đi theo direc thoát khỏi car2
        if car in self.visited:
            return 0

        self.visited.add(car)
        col, row = state[car]
        orientation = self.cars_map[car]['orientation']
        length = self.cars_map[car]['cost']

        #  trục cần thoát
        target_axis = state[car2][1] if self.cars_map[car2]['orientation'] == 'H' else state[car2][0]

        # bị tường chắn
        if direction == 'forward' and target_axis + length >= self.size:
            return float('inf')
        if direction == 'backward' and target_axis < length:
            return float('inf')
        if direction == 'forward':
            step = target_axis + 1 - col if orientation == 'H' else target_axis + 1 - row
        else:
            step = col - (target_axis - length) if orientation == 'H' else row - (target_axis - length)  


        # không bị tường, bị blocker
        blocker = self.get_blocker(state, car, direction, step)
        if blocker:
            forward = self.heuristic2(state, blocker, car, 'forward')
            self.visited.remove(blocker)
            backward = self.heuristic2(state, blocker, car, 'backward')
            self.visited.remove(blocker)
            blocker_cost = min(forward, backward)
            if blocker_cost == float('inf'):
                return float('inf')
            return length * step + blocker_cost

        # không bị blocker 
        return length * step
    
    def get_blocker(self, state: dict, car: str, direction: str, ran: int) -> str:
        """
        Trả về xe gần nhất chặn hướng di chuyển `direction` của `car`
        direction: 'forward' hoặc 'backward'
        """
        col, row = state[car]
        orientation = self.cars_map[car]['orientation']
        length = self.cars_map[car]['cost']

       
        # bắt đầu từ đầu/đuôi xe, di chuyển từng bước để tìm xe chặn
        for step in range(1, ran):
            if orientation == 'H':
                check_col = col + length - 1 + step if direction == 'forward' else col - step
                check_row = row
            else:
                check_row = row + length - 1 + step if direction == 'forward' else row - step
                check_col = col

            if not (0 <= check_row < self.size and 0 <= check_col < self.size):
                break 

            # check xem ô có bị chiếm ko
            for other_car, other_info in self.cars_map.items():
                if other_car == car:
                    continue
                other_col, other_row = state[other_car]
                other_len = other_info['cost']
                other_orient = other_info['orientation']

                # lấy ô của other_car
                if other_orient == 'H':
                    occupied = [(other_row, other_col + i) for i in range(other_len)]
                else:
                    occupied = [(other_row + i, other_col) for i in range(other_len)]

                if (check_row, check_col) in occupied:
                    return other_car  #  xe chặn gần nhất

        return None 
    
    def a_star_solver(self) -> tuple[list[dict], int, int, int]:
        solution = []
        search_time = 0
        memory_usage = 0
        expanded_nodes = 0

        start = default_timer()
        tracemalloc.start()

        state = self.initial_state
        frontier = []
        parent_of = {}
        expanded = set()
        cost_of = {self.hash_state(state): 0}
        counter = 0

        h = self.heuristic(state)
        heapq.heappush(frontier, (h, counter, 0, state))  # (f, tie, g, state)
        counter += 1

        while frontier:
            f_cost, _, g_cost, current_state = heapq.heappop(frontier)

            hashed = self.hash_state(current_state)
            if hashed in expanded:
                continue
            expanded.add(hashed)

            if self.is_goal(current_state):
                expanded_nodes = len(expanded)
                end = default_timer()
                search_time = end - start
                this_state = current_state
                while self.hash_state(this_state) in parent_of:
                    this_cost = cost_of[self.hash_state(this_state)]
                    solution.append({'total_cost': this_cost, 'state': this_state})
                    this_state = parent_of[self.hash_state(this_state)]
                solution.append({'total_cost': 0, 'state': self.initial_state})
                solution = list(reversed(solution))
                memory_size, memory_peak = tracemalloc.get_traced_memory()
                tracemalloc.reset_peak()
                memory_usage = memory_peak
                return (solution, search_time, memory_usage, expanded_nodes)

            for next_state, step_cost in self.get_successors(current_state):
                new_g = g_cost + step_cost
                hashed_next = self.hash_state(next_state)
                if hashed_next not in cost_of or new_g < cost_of[hashed_next]:
                    cost_of[hashed_next] = new_g
                    parent_of[hashed_next] = current_state
                    h = self.heuristic(next_state)
                    heapq.heappush(frontier, (new_g + h, counter, new_g, next_state))
                    counter += 1
        # if no solution
        expanded_nodes = len(expanded)
        end = default_timer()
        search_time = end - start
        memory_size, memory_peak = tracemalloc.get_traced_memory()
        tracemalloc.reset_peak()
        memory_usage = memory_peak
        return (solution, search_time, memory_usage, expanded_nodes)