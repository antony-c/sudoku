import pygame
import pygame.freetype
from constants import Colours


class Box:

    def __init__(self, screen, rect, content):
        self.screen = screen

        self.rect = rect  # Box object

        # Colour constants (R, G, B) & Rendering constants
        self.colours = Colours()
        self.GAME_FONT = pygame.freetype.SysFont('arial', 54)

        self.input = str()  # Content of user input

        self.content = content  # content of each cell

        # If box already filled in, it cannot be edited
        if content:
            self.editable = False
        else:
            self.editable = True

        self.clicked = False  # True if cell clicked

    def draw_box(self):
        pygame.draw.rect(self.screen, self.colours.LIGHT_GREY, self.rect)

    def draw_text(self, input, colour):
        if input is not None:  # If input not empty
            self.content = input

        if self.content:  # If content not empty
            # Render cell content to screen
            self.GAME_FONT.render_to(self.screen,
                                    (self.rect.center[0] - 15, self.rect.center[1] - 18),
                                    str(self.content),
                                    colour)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if any(keys):  # If any keys down
            key = keys.index(True)
            if key in range(30, 39):  # If key is number 1-9
                return key - 29  # Return number

    # Check if box has been clicked
    def check_clicked(self):

        # Function returns True if mouse hovering over cell
        def mouse_in_box(pos):
            if pos[0] > self.rect.left and pos[0] < self.rect.right\
                    and pos[1] > self.rect.top and pos[1] < self.rect.bottom:
                return True
            else:
                return False

        mouse_down = pygame.mouse.get_pressed()[0]  # Check if mouse down
        mouse_pos = pygame.mouse.get_pos()  # Get mouse position

        # Self explanitory
        if mouse_in_box(mouse_pos) and mouse_down:
            self.clicked = True
        elif not mouse_in_box(mouse_pos) and mouse_down:
            self.clicked = False

    def highlight(self):
        rect = pygame.Rect(self.rect.left, self.rect.top, 78, 8)
        pygame.draw.rect(self.screen, self.colours.GREEN, rect)

        rect = pygame.Rect(self.rect.left, self.rect.bottom - 8, 78, 8)
        pygame.draw.rect(self.screen, self.colours.GREEN, rect)

        rect = pygame.Rect(self.rect.left, self.rect.top, 8, 78)
        pygame.draw.rect(self.screen, self.colours.GREEN, rect)

        rect = pygame.Rect(self.rect.right - 8, self.rect.top, 8, 78)
        pygame.draw.rect(self.screen, self.colours.GREEN, rect)

    def update(self):
        self.check_clicked()
        self.draw_box()

        input = None
        # If cell selected, grab input and highlight cell
        if self.clicked and self.editable:
            input = self.get_input()
            self.highlight()

        # If cell filled at the start, cell is black,
        # if cell filled by user, cell is dark blue
        if self.editable:
            self.draw_text(input, self.colours.DARK_BLUE)
        else:
            self.draw_text(input, self.colours.BLACK)
