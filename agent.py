from enum import Enum

class Algorithm(Enum):
    BREATH_FIRST_SEARCH = 0
    ASTAR_SEARCH_1 = 1
    ASTAR_SEARCH_2 = 2

chosen_algorithm = Algorithm.BREATH_FIRST_SEARCH

from sokoban import *
import copy
import sys
import time
from queue import PriorityQueue

class OrderedEnum(Enum):
     def __ge__(self, other):
         if self.__class__ is other.__class__:
             return self.value >= other.value
         return NotImplemented
     def __gt__(self, other):
         if self.__class__ is other.__class__:
             return self.value > other.value
         return NotImplemented
     def __le__(self, other):
         if self.__class__ is other.__class__:
             return self.value <= other.value
         return NotImplemented
     def __lt__(self, other):
         if self.__class__ is other.__class__:
             return self.value < other.value
         return NotImplemented

class Direction(OrderedEnum):
    UP = (0,-1)
    DOWN = (0,1)
    LEFT = (-1,0)
    RIGHT = (1,0)

next_actions = []
steps = 0

def breath_first_search():

    global steps

    visited = set()
    queue = []

    queue.append((copy.deepcopy(game.get_matrix()), []))

    while queue:

        popped = queue.pop(0)

        current = popped[0]
        current_as_string = '%'.join('!'.join(line) for line in current)
        actions = popped[1]

        steps += 1

        print(actions)

        if current_as_string in visited:
            continue

        game.set_matrix(current)

        if game.is_completed():
            print(actions)
            return actions

        visited.add(current_as_string)

        saved_state = copy.deepcopy(current)

        for dir in Direction:
            game.move(dir.value[0], dir.value[1], False)
            new_actions = copy.deepcopy(actions)
            new_actions.append(dir)
            queue.append((copy.deepcopy(game.get_matrix()), new_actions))
            game.set_matrix(saved_state)
            saved_state = copy.deepcopy(saved_state)

def distance(point_a, point_b):
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])

def h_function(matrix):

    boxes = []
    goals = []

    x = 0
    y = 0
    for row in matrix:
        for char in row:
            if char == '$':
                boxes.append((x,y))
            if char == '.':
                goals.append((x,y))
            x = x + 1
        x = 0
        y = y + 1

    total_dist = 0

    for box in boxes:
        best_dist = 100000
        for goal in goals:
            if chosen_algorithm == Algorithm.ASTAR_SEARCH_2:
                total_dist += distance(box, goal)
            elif chosen_algorithm == Algorithm.ASTAR_SEARCH_1:
                best_dist = min(best_dist, distance(box, goal))

        if chosen_algorithm == Algorithm.ASTAR_SEARCH_1:
            total_dist += best_dist

    return 100 * total_dist

def astar_search():

    global steps

    visited = set()
    queue = PriorityQueue()

    queue.put((0 + h_function(game.get_matrix()), (0, (copy.deepcopy(game.get_matrix()), []))))

    while queue:

        popped_temp = queue.get()[1]

        print("X " + str(popped_temp))

        popped = popped_temp[1]
        cost_so_far = popped_temp[0] + 1

        current = popped[0]
        current_as_string = '%'.join('!'.join(line) for line in current)
        actions = popped[1]

        steps += 1

        print("TESTT " + str(steps))
        print(actions)

        if current_as_string in visited:
            continue

        game.set_matrix(current)

        if game.is_completed():
            print(actions)
            return actions

        visited.add(current_as_string)

        saved_state = copy.deepcopy(current)

        for dir in Direction:
            game.move(dir.value[0], dir.value[1], False)
            new_actions = copy.deepcopy(actions)
            new_actions.append(dir)
            queue.put((cost_so_far + h_function(game.get_matrix()), (cost_so_far, (copy.deepcopy(game.get_matrix()), new_actions))))
            game.set_matrix(saved_state)
            saved_state = copy.deepcopy(saved_state)


initial_state = game.get_matrix().copy()

if chosen_algorithm == Algorithm.ASTAR_SEARCH_1 or chosen_algorithm == Algorithm.ASTAR_SEARCH_2:
    next_actions = astar_search()
elif chosen_algorithm == Algorithm.BREATH_FIRST_SEARCH:
    next_actions = breath_first_search()

game.set_matrix(initial_state)

print(next_actions)

while 1:
    if game.is_completed(): display_end(screen)
    print_game(game.get_matrix(),screen)
    print(game.get_matrix())
    time.sleep(0.25)
    if len(next_actions) != 0:
        game.move(next_actions[0].value[0], next_actions[0].value[1], True)
        next_actions.remove(next_actions[0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q: sys.exit(0)
            elif event.key == pygame.K_d: game.unmove()
    pygame.display.update()