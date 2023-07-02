import pygame

pygame.init()

from maze_mapper.maze import Maze
from maze_mapper.utils import WHITE


# Open a new window
size = (1000, 1000)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Maze")

# The loop will carry on until the user exits the game (e.g. clicks the close button).
loop = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

maze = Maze(20, 20, 50)
maze.randomise()

selected = (-1, -1)

while loop:
    # --- Main event loop
    maze.unhighlight()

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            loop = False  # Flag that we are done so we can exit the while loop
        if event.type == pygame.MOUSEMOTION:
            # If user moved the mouse and mouse is on the screen
            mouse_position = pygame.mouse.get_pos()

            x = mouse_position[0] // maze.cell_size
            y = mouse_position[1] // maze.cell_size

            selected = (x, y)

    if pygame.mouse.get_focused():
        maze[selected[0]][selected[1]].highlighted = True

    # --- Game logic should go here

    # --- Drawing code should go here

    # First, clear the screen to white.
    screen.fill(WHITE)

    maze.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
