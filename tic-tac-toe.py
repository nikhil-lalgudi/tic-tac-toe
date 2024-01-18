#!/usr/bin/env python
# coding: utf-8

import pygame
import numpy as np
import random
import sys

# Initialize pygame
pygame.init()

# Constants
width, height = 300, 300
rows, cols = 3, 3
square_size = width // cols

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Initialize the game window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tic Tac Toe")

# Fonts
font = pygame.font.SysFont(None, 55)

# Board
board = np.zeros((rows, cols))

def draw_board():
    screen.fill(white)
    for row in range(1, rows):
        pygame.draw.line(screen, black, (0, row * square_size), (width, row * square_size), 2)
    for col in range(1, cols):
        pygame.draw.line(screen, black, (col * square_size, 0), (col * square_size, height), 2)

def draw_symbols():
    for row in range(rows):
        for col in range(cols):
            if board[row, col] == 1:
                draw_x(col, row)
            elif board[row, col] == -1:
                draw_o(col, row)

def draw_x(col, row):
    pygame.draw.line(screen, black, (col * square_size, row * square_size),
                     ((col + 1) * square_size, (row + 1) * square_size), 2)
    pygame.draw.line(screen, black, ((col + 1) * square_size, row * square_size),
                     (col * square_size, (row + 1) * square_size), 2)

def draw_o(col, row):
    pygame.draw.circle(screen, black, (col * square_size + square_size // 2, row * square_size + square_size // 2),
                       square_size // 2 - 5, 2)

def is_board_full():
    return np.all(board != 0)

def is_winner(player):
    return np.any(np.all(board == player, axis=0)) or np.any(np.all(board == player, axis=1)) or \
           np.all(np.diag(board) == player) or np.all(np.diag(np.fliplr(board)) == player)

def get_empty_cells():
    return [(i, j) for i in range(rows) for j in range(cols) if board[i, j] == 0]

def player_move(row, col):
    if board[row, col] == 0:
        board[row, col] = 1
        return True
    return False

def ai_move():
    empty_cells = get_empty_cells()

    # Check if AI can win in the next move
    for cell in empty_cells:
        row, col = cell
        board[row, col] = -1
        if is_winner(-1):
            pygame.time.delay(500)  # Introduce delay before showing the winning move
            return row, col
        board[row, col] = 0  # Undo the move

    # Check if player can win in the next move and block them
    for cell in empty_cells:
        row, col = cell
        board[row, col] = 1
        if is_winner(1):
            board[row, col] = -1  # Block the player
            return row, col
        board[row, col] = 0  # Undo the move

    # If no immediate win/lose move, make a strategic move
    strategic_move = strategic_ai_move()
    if strategic_move:
        return strategic_move

    # If no strategic move, choose a random move
    if empty_cells:
        return random.choice(empty_cells)

def strategic_ai_move():
    # Placeholder for a more advanced strategy.
    # This example prioritizes the center, then corners, then edges.
    if (1, 1) in get_empty_cells():
        return 1, 1  # Center

    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for corner in corners:
        if corner in get_empty_cells():
            return corner  # Corners

    edges = [(0, 1), (1, 0), (1, 2), (2, 1)]
    for edge in edges:
        if edge in get_empty_cells():
            return edge  # Edges

    return None

def reset_game():
    global board, player_turn
    board = np.zeros((rows, cols))
    player_turn = True

def show_popup(message):
    pygame.time.delay(500)  # Introduce delay before showing the popup
    pygame.display.set_caption("Game Over")
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                reset_game()
                return

        pygame.display.set_caption(message)
        pygame.display.flip()

# Main game loop
running = True
player_turn = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and player_turn:
            mouseX, mouseY = event.pos
            col = mouseX // square_size
            row = mouseY // square_size

            if player_move(row, col):
                player_turn = False

    draw_board()
    draw_symbols()

    if not player_turn:
        ai_move_result = ai_move()
        if ai_move_result is not None:
            ai_row, ai_col = ai_move_result
            board[ai_row, ai_col] = -1
            draw_board()  # Redraw the board after AI's final move
            pygame.display.flip()  # Update the display
            pygame.time.delay(500)  # Introduce delay before showing the result

            if is_winner(-1):
                show_popup("AI wins! Click to start a new game.")
            elif is_board_full():
                show_popup("It's a tie! Click to start a new game.")
            else:
                player_turn = True

    pygame.display.flip()

    if is_winner(1):
        show_popup("Player wins! Click to start a new game.")
    elif is_board_full():
        show_popup("It's a tie! Click to start a new game.")

    pygame.time.Clock().tick(30)  # Adjust the clock tick for smoother gameplay

# Quit pygame
pygame.quit()
sys.exit()

