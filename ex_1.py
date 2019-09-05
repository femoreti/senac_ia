from math import inf as infinity
from random import choice
import platform
import time
import random
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


def OnGiveScore(p_board):
    """
    Calcula uma heuristica para estado do jogo
    :param p_board: o estado atual do jogo
    :return: +1 para vitoria da IA; -1 para vitoria do jogador; 0 em caso de empate
    """
    if OnCheckForWin(p_board, COMP):
        score = +1
    elif OnCheckForWin(p_board, player):
        score = -1
    else:
        score = 0

    return score


def OnCheckForWin(p_board, p_user):
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


def OnGameOver(p_board):
    """
    Metodo que retorna quem venceu
    :param p_board: o estado do tabuleiro
    :return: True caso alguem tenha vencido
    """
    return OnCheckForWin(p_board, player) or OnCheckForWin(p_board, COMP)


def OnGetEmptyCells(state):
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
    verifica se a celula escolhida esta vazia
    """
    if [x, y] in OnGetEmptyCells(board):
        return True
    else:
        return False


def OnWriteOnBoard(x, y, player):
    """
    se a celula estiver vazia realiza o movimento
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(p_board, depth, player):
    """
    Metodo minimax para avaliar os estados da IA
    :param p_board: o estado do jogo atual
    :param depth: index atual da arvore
    :param player: Jogador ou IA
    :return: uma lista contendo [melhor linha, melhor coluna, melhor score]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or OnGameOver(p_board):
        score = OnGiveScore(p_board)
        return [-1, -1, score]

    for cell in OnGetEmptyCells(p_board):
        x, y = cell[0], cell[1]
        p_board[x][y] = player
        score = minimax(p_board, depth - 1, -player)
        p_board[x][y] = 0
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


def print_board(p_board, ia_letter, player_letter):
    """
    Desenha o jogo na tela
    :param p_board: tabuleiro
    """

    chars = {
        -1: player_letter,
        +1: ia_letter,
        0: ' '
    }
    str_line = '==============='

    print('\n' + str_line)
    for row in p_board:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def OnIATurn(ia_letter, player_letter):

    depth = len(OnGetEmptyCells(board))
    if depth == 0 or OnGameOver(board):
        return

    ClearConsole()
    print(f'Vez da IA [{ia_letter}]')
    print_board(board, ia_letter, player_letter)

    if depth == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        move = minimax(board, depth, COMP)
        x, y = move[0], move[1]

    OnWriteOnBoard(x, y, COMP)
    time.sleep(1)


def OnPlayerTurn(ia_letter, player_letter):
    depth = len(OnGetEmptyCells(board))
    if depth == 0 or OnGameOver(board):
        return

    # cria dicionario com movimentos validos
    move = -1
    boardCells = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    ClearConsole()
    print(f'turno do jogador [{player_letter}]')
    print_board(board, ia_letter, player_letter) #desenha o tabuleiro escrevendo os caracteres preenchidos com X ou O

    while move < 1 or move > 9:
        try:
            move = int(input('Digite um valor de 1 a 9: '))
            coord = boardCells[move]
            can_move = OnWriteOnBoard(coord[0], coord[1], player)

            if not can_move:
                print('Celula ja foi preenchida, tente outra')
                move = -1
        except (EOFError, KeyboardInterrupt):
            ClearConsole()
            exit()
        except (KeyError, ValueError):
            print('Caracter invalido, Digite um valor de 1 a 9')


def main():

    ClearConsole()
    player_letter = ''  # X or O
    ia_letter = ''  # X or O
    first = ''

    #jogador escolhe sua letra
    while player_letter != 'O' and player_letter != 'X':
        try:
            print('')
            player_letter = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            exit()
        except (KeyError, ValueError):
            print('Caractere invalido, use X ou O')

    # Determina os caracteres
    if player_letter == 'X':
        ia_letter = 'O'
    else:
        ia_letter = 'X'

    # Define quem comeca primeiro
    ClearConsole()

    if random.randint(0, 1) == 1:
         first = 'N'
    else:
         first = 'Y'    

    # Execucao do jogo
    while len(OnGetEmptyCells(board)) > 0 and not OnGameOver(board):
        if first == 'N':
            OnIATurn(ia_letter, player_letter)
            first = ''

        OnPlayerTurn(ia_letter, player_letter)
        OnIATurn(ia_letter, player_letter)

    # Imprime mensagem de fim de jogo
    if OnCheckForWin(board, player):
        ClearConsole()
        print(f'Sua vez [{player_letter}]')
        print_board(board, ia_letter, player_letter)
        print('Vitória, Voce ganhou!')
    elif OnCheckForWin(board, COMP):
        ClearConsole()
        print(f'Vez da IA [{ia_letter}]')
        print_board(board, ia_letter, player_letter)
        print('Derrota, a IA ganhou!')
    else:
        ClearConsole()
        print_board(board, ia_letter, player_letter)
        print('Empate!')

    exit()


if __name__ == '__main__':
    main()