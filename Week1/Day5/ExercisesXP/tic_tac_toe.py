def new_board():
    return [[' ' for _ in range(3)]for _ in range(3)]


def show_board(board):
    print('***************')
    for r, row in enumerate(board, start=1):
        print(f"*  " + " | ".join(row), ' *')
        if r < 3:
            print("* ---+---+--- *")
    print('***************')
    print()


def is_valid_move(board, r, c):
    return 1 <= r <= 3 and 1 <= c <= 3 and board[r-1][c-1] == ' '


def player_input(current, board):
    while True:
        try:
            raw = input(
                f"Player {current}, enter row and column (like '2' '3') : ").strip()
            parts = raw.split()
            if len(parts) != 2:
                raise ValueError
            r, c = map(int, parts)
            if not is_valid_move(board, r, c):
                print(
                    'Invalid move. Make sure it is within 1 to 3 and the cell is empty!')
                continue
            return r-1, c-1
        except:
            print('Please enter two integers between 1 and 3 (e.g. 1 3)')


def switch_player(player):
    return 'O' if player == 'X' else 'X'


def check_win(board, current):
    lines = []

    # Horizontal and vertical check
    lines.extend(board)  # rows
    lines.extend([[board[r][c]for r in range(3)] for c in range(3)])  # columns

    # diagonals check
    lines.append([board[i][i]for i in range(3)])
    lines.append([board[i][2-i]for i in range(3)])

    return any(all(cell == current for cell in line) for line in lines)


def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)


def main():
    print('\nWelcome to TIC TAC TOE!\n')
    board = new_board()
    current = 'X'
    show_board(board)

    while True:
        r, c = player_input(current, board)
        board[r][c] = current
        show_board(board)
        if check_win(board, current):
            print(f'Player {current} wins!')
            break
        if check_draw(board):
            print('It is a draw. Try to play again ;)')
            break
        current = switch_player(current)


main()
