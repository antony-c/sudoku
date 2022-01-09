import sudoku
import pygame

grid = sudoku.Generate()  # Generate Sudoku board

# Initiate pygame
pygame.init()
size = (818, 900)
screen = pygame.display.set_mode(size)

game = sudoku.Gui(screen, grid.unsolved, grid.solved)  # Initiate GUI

game.start()  # Initiate Game
