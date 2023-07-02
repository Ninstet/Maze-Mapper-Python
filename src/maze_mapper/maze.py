import pygame
import random

from maze_mapper.utils import FONT, BLACK, GREEN


class Cell:
    """
    A cell in the maze.

    A maze "Cell" is a point in the grid which may be surrounded by walls to
    the north, east, south or west.
    """

    # A wall separates a pair of cells in the N-S or W-E directions
    wall_pairs = {"N": "S", "S": "N", "E": "W", "W": "E"}

    def __init__(self, x, y, size: int = 50):
        """
        Initialise the cell at (x, y) with a specified pixel size.

        Assume the cell is surrounded by walls to the north, east, south and west.
        """

        self.x, self.y = x, y
        self.size = size

        self.walls = {"N": True, "S": True, "E": True, "W": True}

        self._highlighted = False

    def __str__(self):
        return self.__class__.__name__ + f"({self.x}, {self.y})"

    def __repr__(self):
        return self.__class__.__name__ + f"({self.x}, {self.y})"

    @property
    def highlighted(self):
        return self._highlighted

    @highlighted.setter
    def highlighted(self, value):
        self._highlighted = value

    def has_all_walls(self) -> bool:
        """
        Check if the cell still has all it's walls.
        """

        return all(self.walls.values())

    def knock_down(self, other_cell, wall: str):
        """
        Knock down the wall between this cell and another cell
        """

        self.walls[wall] = False
        other_cell.walls[Cell.wall_pairs[wall]] = False

    def draw(self, screen, show_cell_text: bool = False):
        """
        Draw the cell to a screen.
        """

        pos_x = self.x * self.size
        pos_y = self.y * self.size

        if self.highlighted:
            pygame.draw.rect(screen, GREEN, (pos_x, pos_y, self.size, self.size))

        for wall in self.walls:
            if not self.walls[wall]:
                continue

            match wall:
                case "N":
                    pygame.draw.line(
                        screen,
                        BLACK,
                        (pos_x, pos_y),
                        (pos_x + self.size, pos_y),
                        3,
                    )
                case "S":
                    pygame.draw.line(
                        screen,
                        BLACK,
                        (pos_x, pos_y + self.size),
                        (pos_x + self.size, pos_y + self.size),
                        3,
                    )
                case "E":
                    pygame.draw.line(
                        screen,
                        BLACK,
                        (pos_x + self.size, pos_y),
                        (pos_x + self.size, pos_y + self.size),
                        3,
                    )
                case "W":
                    pygame.draw.line(
                        screen,
                        BLACK,
                        (pos_x, pos_y),
                        (pos_x, pos_y + self.size),
                        3,
                    )

        if show_cell_text:
            cell_text = FONT.render(f"({self.x}, {self.y})", False, BLACK)
            screen.blit(cell_text, (pos_x + 5, pos_y + 5))


class Maze:
    def __init__(self, no_rows: int, no_columns: int, cell_size: int):
        self.no_rows, self.no_columns = no_rows, no_columns
        self.cell_size = cell_size

        self.cells = [
            Cell(i % no_rows, i // no_columns, cell_size)
            for i in range(no_rows * no_columns)
        ]

    def __getitem__(self, column: int):
        """
        Return a row of the maze.
        """

        if column > self.no_columns:
            return []

        return self.cells[column : self.no_rows * self.no_columns : self.no_rows]

    def unhighlight(self):
        """
        Unhighlight all cells in the maze.
        """

        for cell in self.cells:
            cell.highlighted = False

    def draw(self, screen):
        for cell in self.cells:
            cell.draw(screen)

    def find_valid_neighbours(self, cell):
        """
        Return a list of unvisited neighbours to a cell.
        """

        delta = [("W", (-1, 0)), ("E", (1, 0)), ("S", (0, 1)), ("N", (0, -1))]

        neighbours = []

        for direction, (dx, dy) in delta:
            x2, y2 = cell.x + dx, cell.y + dy  # Position of next cell

            if (0 <= x2 < self.no_rows) and (0 <= y2 < self.no_columns):
                neighbour = self[x2][y2]

                if neighbour.has_all_walls():
                    neighbours.append((direction, neighbour))

        return neighbours

    def randomise(self):
        """
        Randomise the maze.
        """

        cell_stack = []
        current_cell = self[0][0]  # Top left cell in the maze
        no_visited = 1

        # While we haven't visited all the cells
        while no_visited < self.no_rows * self.no_columns:
            neighbours = self.find_valid_neighbours(current_cell)

            if not neighbours:
                # No neighbours which means we've reached a deadend, so backtrack
                current_cell = cell_stack.pop()
                continue

            # Choose a random neighbouring cell and move to it
            direction, next_cell = random.choice(neighbours)

            current_cell.knock_down(next_cell, direction)
            cell_stack.append(current_cell)

            current_cell = next_cell
            no_visited += 1
