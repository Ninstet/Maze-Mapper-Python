from maze_mapper.algorithm import Algorithm
from maze_mapper.maze import Maze


class A_Star(Algorithm):
    def solve(self, start_cell, end_cell):
        current_node = start_cell

        open_list = [start_cell]
        closed_list = []

        path_found = False

        while not path_found:
            if min(nodes) == end_cell:
                # We are finished
                path_found = True
                break

            else:
                closed_list.append(current_node)

                for neighbour in self._maze.find_valid_neighbours(current_node):
                    if neighbour.g < current_node.g and neighbour in closed_list:
                        