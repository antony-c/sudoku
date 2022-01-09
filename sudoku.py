from random import randint, choice as randchoice
from time import time as current_time
from datetime import timedelta
from input import Box
from constants import Colours
import pygame
import pygame.freetype
import sys


class Generate:

    def __init__(self):
        # Modify table into sudoku
        self.solved = self.make_grid()

        # Remove some cells so that player must fill puzzle
        self.unsolved = self.unsolve()

    def make_grid(self, table=None):
        # If table not generated (not passed as argument, 1st recursion)
        # Generate blank 9x9 grid, grid will be modified into sudoku puzzle
        if table is None:
            table = [[0 for j in range(9)] for i in range(9)]

        # Intuitive algorithm to find 3x3 unit from x & y coordinates
        def get_unit(x, y):
            x_start = x // 3 * 3
            y_start = y // 3 * 3

            x_range = range(x_start, x_start + 3)
            y_range = range(y_start, y_start + 3)

            return [table[i][j] for j in y_range for i in x_range]

        # Returns all possible values for cell
        def avail_vals(x, y):
            row = table[x]  # Values in row
            col = [table[e][y] for e in range(9)]  # Values in column
            unit = get_unit(x, y)  # Values in 3x3 unit

            sections = [row, col, unit]  # Saving code from too many "if and"s

            # Return number if number is not in any conflicting sections
            def conflicting(i):
                return any(i in section for section in sections)

            return [i for i in range(1, 10) if not conflicting(i)]

        # Iterate through every cell in blank soduku
        for i, row in enumerate(table):
            for j, cell in enumerate(row):
                available_values = avail_vals(i, j)
                # If no available values and row not full, recurse & reset row
                if not available_values and not all(row):
                    # Reset current row
                    table[i] = [0 for _ in range(9)]
                    return self.make_grid(table)
                # Else if cell is 0 (not assigned a value)
                if not table[i][j]:
                    # Assign a random available value to cell
                    table[i][j] = randchoice(available_values)
        return table

    def unsolve(self):
        # Returns value to fill cell with.
        # If random number is 1, cell stays solved
        # If random number is 0, cell becomes unsolved (0), player must fill in
        def chance(cell):
            return cell if randint(0, 1) else 0

        # Run chance function for each cell in sudoku puzzle
        return [[chance(cell) for cell in row] for row in self.solved]


class Gui:

    def __init__(self, screen, unsolved_grid, solved_grid):
        self.screen = screen

        # Soduku game grids
        self.unsolved_grid = unsolved_grid
        self.solved_grid = solved_grid

        self.boxes = self.init_boxes()  # Initialize input boxes

        # Colour constants (R, G, B) & Rendering constants
        self.colours = Colours()
        self.GAME_FONT = pygame.freetype.SysFont('arial', 34)

        # Game variables
        self.start_time = current_time()

    def start(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.update()  # Update screen every loop

    def update(self):
        self.screen.fill(self.colours.BLACK)

        self.display_clock()  # Display time elapsed
        self.draw_board()  # Draw Sudoku board

        pygame.display.flip()

    def display_clock(self):

        # Function for converting number of seconds to formatted version.
        # I.E. 65 seconds = 1:05
        def format_time(seconds):
            return str(timedelta(seconds=seconds))

        # Formatted number of seconds
        formatted = format_time(int(current_time() - self.start_time))

        self.GAME_FONT.render_to(self.screen,
                                    (305, 25),
                                    f"{formatted[2::]} elapsed",
                                    self.colours.WHITE)

    def draw_board(self):
        # Draw each square as 78 pixels, lines as 10px, every third line as 14px
        # How do I can't even explain this algorithm with comments
        # I like to do math instead of too many if statements to avoid slow code
        # Trust me it works though

        def draw_lines():
            width = 0
            start = 0

            for i in range(10):
                x = (i % 3 - 1) * 2 + 1
                y = abs((x / abs(x) - 1) / 2) * 14
                z = ((x / abs(x) + 1) / 2) * 10
                width = int(y + z)

                rectangle = pygame.Rect(start, 82, width, 900)
                pygame.draw.rect(self.screen, self.colours.GREY, rectangle)

                rectangle = pygame.Rect(0, start + 82, 900, width)
                pygame.draw.rect(self.screen, self.colours.GREY, rectangle)

                start += (78 + width)

        def draw_boxes():
            for i, row in enumerate(self.boxes):
                for j, box in enumerate(row):
                    box.update()  # Update box
                    # If player inputs incorrect answer into cell
                    if box.content is not None\
                            and box.content != self.solved_grid[i][j]:
                        box.content = None

        draw_lines()
        draw_boxes()

    def init_boxes(self):
        boxes = list()

        # Function that assists in returning where each box
        # should be placed on board
        def get_width(val):
            x = (val % 3 - 1) * 2 + 1
            y = abs((x / abs(x) - 1) / 2) * 14
            z = ((x / abs(x) + 1) / 2) * 10
            width = int(y + z)
            return width

        # Function that returns where each box should be placed on board
        def next_coords(val):
            x = (val % 3 - 1) * 2 + 1
            y = abs((x / abs(x) - 1) / 2) * 14
            z = ((x / abs(x) + 1) / 2) * 10
            width1 = int(y + z)
            return 78 + width1

        start1 = 0
        start2 = 0

        # Generate one input box for each cell
        for i in range(9):
            width1 = get_width(i)
            boxes.append([])
            for j in range(9):
                width2 = get_width(j) + 82

                rect = pygame.Rect(start1 + width1, start2 + width2, 78, 78)

                # Respective value of soduku cell at index
                value = self.unsolved_grid[i][j]
                boxes[i].append(Box(self.screen, rect, value))

                start2 += next_coords(j)

            start1 += next_coords(i)
            start2 = 0

        return boxes
