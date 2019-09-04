#!/usr/bin/env python3
from math import inf as infinity
from random import choice
import platform
import time
from os import system

"""
Jogo da velha usando MiniMax
"""

player = -1
COMP = +1
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def evaluate(p_board):
    """
    Function to heuristic evaluation of state.
    :param p_board: the state of the current board
    :return: +1 para vitoria da IA; -1 para vitoria do jogador; 0 em caso de empate
    """
    if wins(p_board, COMP):
        score = +1
    elif wins(p_board, player):
        score = -1
    else:
        score = 0

    return score


def wins(p_board, p_user):
    """
    Metodo que verifica se eh um estado de vitoria
    :param p_board: o estado do tabuleiro
    :param p_user: o jogador ou a IA
    :return: True se for vitoria
    """
    win_state = [
        [p_board[0][0], p_board[0][1], p_board[0][2]],
        [p_board[1][0], p_board[1][1], p_board[1][2]],
        [p_board[2][0], p_board[2][1], p_board[2][2]],
        [p_board[0][0], p_board[1][0], p_board[2][0]],
        [p_board[0][1], p_board[1][1], p_board[2][1]],
        [p_board[0][2], p_board[1][2], p_board[2][2]],
        [p_board[0][0], p_board[1][1], p_board[2][2]],
        [p_board[2][0], p_board[1][1], p_board[0][2]],
    ]
    if [p_user, p_user, p_user] in win_state:
        return True
    else:
        return False


def game_over(p_board):
    """
    Metodo que retorna quem venceu
    :param p_board: o estado do tabuleiro
    :return: True caso alguem tenha vencido
    """
    return wins(p_board, player) or wins(p_board, COMP)


def empty_cells(state):
    """
    Each empty cell will be added into cells' list
    :param state: the state of the current board
    :return: a list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    """
    A move is valid if the chosen cell is empty
    :param x: X coordinate
    :param y: Y coordinate
    :return: True if the board[x][y] is empty
    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
    Set the move on board, if the coordinates are valid
    :param x: X coordinate
    :param y: Y coordinate
    :param player: the current player
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player):
    """
    AI function that choice the best move
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see iaturn() function)
    :param player: an player or a computer
    :return: a list with [the best row, best col, best score]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def ClearConsole():
    """
    Limpa o console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def print_board(p_board, c_choice, h_choice):
    """
    Desenha o jogo na tela
    :param p_board: tabuleiro
    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in p_board:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    """
    It calls the minimax function if the depth < 9,
    else it choices a random coordinate.
    :param c_choice: computer's choice X or O
    :param h_choice: player's choice X or O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    ClearConsole()
    print(f'Computer turn [{c_choice}]')
    print_board(board, c_choice, h_choice)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)


def player_turn(c_choice, h_choice):
    """
    The player plays choosing a valid move.
    :param c_choice: computer's choice X or O
    :param h_choice: player's choice X or O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    ClearConsole()
    print(f'turno do jogador [{h_choice}]')
    print_board(board, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], player)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')


def main():
    """
    Main function that calls all functions
    """
    ClearConsole()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if player is the first

    # player chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # player may starts first
    ClearConsole()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Main loop of this game
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''

        player_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)

    # Game over message
    if wins(board, player):
        ClearConsole()
        print(f'Sua vez [{h_choice}]')
        print_board(board, c_choice, h_choice)
        print('Vitória, Voce ganhou!')
    elif wins(board, COMP):
        ClearConsole()
        print(f'Vez da IA [{c_choice}]')
        print_board(board, c_choice, h_choice)
        print('Derrota, a IA ganhou!')
    else:
        ClearConsole()
        print_board(board, c_choice, h_choice)
        print('Empate!')

    exit()


if __name__ == '__main__':
    main()