import pygame.event

from sokoban import *
import time
import copy

from enum import Enum
class Direction(Enum):
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

        print("AT STEP " + str(steps))
        print(actions)
        print("HERE " + current_as_string)

        if current_as_string in visited:
            continue

        game.set_matrix(current)

        #print("LOL " + current_as_string + " + " + str(game.is_completed()))

        if game.is_completed():
            print("RETURNED")
            print(actions)
            return actions

        visited.add(current_as_string)

        saved_state = copy.deepcopy(current)

        for dir in Direction:
            #print("GOING FROM " + str(dir))
            #print(game.get_matrix())
            #print("XDD " + str(dir) + " + " + str(game.can_move(dir.value[0], dir.value[1])))
            #print(game.get_matrix())
            #print(current)
            game.move(dir.value[0], dir.value[1], False)
            #print(game.get_matrix())
            #print(current)
            #print(test)
            #print("TO")
            #print(game.get_matrix())
            #print("")
            #print("")
            new_actions = copy.deepcopy(actions)
            new_actions.append(dir)
            queue.append((copy.deepcopy(game.get_matrix()), new_actions))
            game.set_matrix(saved_state)
            saved_state = copy.deepcopy(saved_state)
            #print(current)
            #print(game.get_matrix())

initial_state = game.get_matrix().copy()

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