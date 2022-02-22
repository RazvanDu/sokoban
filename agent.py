from sokoban import *
import time

from enum import Enum
class Direction(Enum):
    UP = (0,-1)
    DOWN = (0,1)
    LEFT = (-1,0)
    RIGHT = (1,0)

next_actions = []

next_actions.append(Direction.UP)
next_actions.append(Direction.UP)
next_actions.append(Direction.UP)
next_actions.append(Direction.UP)
next_actions.append(Direction.LEFT)
next_actions.append(Direction.LEFT)
next_actions.append(Direction.UP)

while 1:
    if game.is_completed(): display_end(screen)
    print_game(game.get_matrix(),screen)
    time.sleep(1)
    if len(next_actions) != 0:
        game.move(next_actions[0].value[0], next_actions[0].value[1], True)
        next_actions.remove(next_actions[0])
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q: sys.exit(0)
            elif event.key == pygame.K_d: game.unmove()
    pygame.display.update()