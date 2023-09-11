def is_empty(board):
    for rows in board:
        if ('b' or 'w') in rows:
            return False
    return True


def is_sq_in_board(board, y, x):
    if y < len(board) and x < len(board[0]) and x >= 0 and y >= 0:
        return True
    else:
        return False


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    # open: element n-1 and n+1 are free squares
    # semi-open: if one of element n-1 or n+1 is a free square
    # closed: if both n-1 and n+1 are not open
    # n+1 element exists
    if is_sq_in_board(board, y_end + d_y, x_end + d_x) and x_end >= 0 and y_end >= 0:
        # n-1 element exists

        if is_sq_in_board(board, y_end - d_y*(length), x_end - d_x*(length)):
            if board[y_end+d_y][x_end+d_x] == " " and board[y_end - d_y*(length)][x_end - d_x*(length)] == " ":

                return "OPEN"
            elif board[y_end+d_y][x_end+d_x] == " " or board[y_end - d_y*(length)][x_end - d_x*(length)] == " ":

                return "SEMIOPEN"
            else:
                return "CLOSED"
        else:
            if board[y_end+d_y][x_end+d_x] == " ":

                return "SEMIOPEN"

            else:
                return "CLOSED"
    else:  # n+ 1 element does not exist, can only be semiopen or closed

        if is_sq_in_board(board, y_end - d_y*(length), x_end - d_x*(length)) and x_end >= 0 and y_end >= 0:
            if board[y_end - d_y*(length)][x_end - d_x*(length)] == " ":

                return "SEMIOPEN"
            else:
                return "CLOSED"

        else:  # n + 1 and n -1 element does not exist
            return "CLOSED"


def is_sequence_complete(board, col, y_start, x_start, length, dy, dx):
    if is_sq_in_board(board, y_start, x_start):
        i = 0
        while i < length:
            if board[y_start+dy*i][x_start+dx*i] != col:
                return False
            i += 1

        # checking for endings of the columns
        if dx == 0:
            if y_start + dy*length >= 8:  # case where we can't check end y or end x
                if board[y_start-dy][x_start] != col:
                    return True
                else:
                    return False
            elif y_start == 0:  # case where we can't check start y
                if board[y_start+dy*length][x_start] != col:
                    return True
                else:
                    return False
            else:
                if board[y_start+dy*length][x_start] != col and board[y_start-dy][x_start] != col:
                    return True
                else:
                    return False

        if dy == 0:
            if x_start + dx*length >= 8:
                if board[y_start][x_start-dx] != col:
                    return True
                else:
                    return False

            elif x_start == 0:  # case where we can't check start x
                if board[y_start][x_start+dx*length] != col:
                    return True
                else:
                    return False

            else:
                if board[y_start][x_start+dx*length] != col and board[y_start][x_start-dx] != col:
                    return True
                else:
                    return False
        else:
            pass

        if dy != 0 and dx != 0:
            n_plus = is_sq_in_board(
                board, y_start+dy*length, x_start+dx*length)
            n_minus = is_sq_in_board(board, y_start-dy, x_start-dx)

            if n_plus == False and n_minus == False:  # cannot check n-1 # cannot check n+1
                return True

            elif n_plus == False:  # cannot check n+1 # can check n-1
                if board[y_start-dy][x_start-dx] != col:
                    return True
                else:
                    return False

            elif n_minus == False:  # cannot check n-1 # can check n+1
                if board[y_start+dy*length][x_start+dx*length] != col:
                    return True
                else:
                    return False

            elif y_start == 0 or x_start == 0:  # cannot check n-1 # can check n+1
                if board[y_start+dy*length][x_start+dx*length] != col:
                    return True
                else:
                    return False

            else:  # can check n-1 # can check n+1
                if board[y_start-dy][x_start-dx] != col and board[y_start+dy*length][x_start+dx*length] != col:
                    return True
                else:
                    return False
    else:
        return False


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    # goes through a row starting at an edge and returns the number of open sequences of length L and the number of semi open seqiences of length L
    open_seq_count = 0
    semi_open_seq_count = 0
    for i in range(8):
        if x_start >= 0 and y_start >= 0 and x_start+d_x*i + d_x*length < 9 and y_start+d_y*i + d_y*length < 9 and is_sequence_complete(board, col, y_start+d_y*i, x_start+d_x*i, length, d_y, d_x):

            state = is_bounded(board, y_start + d_y * i + d_y * (length-1),
                               x_start+d_x*i + d_x*(length-1), length, d_y, d_x)
            if state == "OPEN":
                open_seq_count += 1
            elif state == "SEMIOPEN":
                semi_open_seq_count += 1
            else:
                None
    return open_seq_count, semi_open_seq_count


"""def detect_row_closed_5(board, col, y_start, x_start, length, d_y, d_x):
    # goes through a row starting at an edge and returns the number of open sequences of length L and the number of semi open seqiences of length L
    closed_seq_5 = 0
    for i in range(8):
        if x_start >= 0 and y_start >= 0 and x_start+d_x*i + d_x*length < 9 and y_start+d_y*i + d_y*length < 9 and is_sequence_complete(board, col, y_start+d_y*i, x_start+d_x*i, length, d_y, d_x):
            state = is_bounded(board, y_start + d_y * i + d_y * (length-1),
                               x_start+d_x*i + d_x*(length-1), length, d_y, d_x)
            if state == "CLOSED":
                closed_seq_5 += 1
            else:
                None
    return closed_seq_5
"""


def detect_row_closed(board, col, y_start, x_start, length, d_y, d_x):
    # goes through a row starting at an edge and returns the number of open sequences of length L and the number of semi open seqiences of length L
    closed_seq_count = 0
    for i in range(8):
        if x_start >= 0 and y_start >= 0 and x_start+d_x*i + d_x*length < 9 and y_start+d_y*i + d_y*length < 9 and is_sequence_complete(board, col, y_start+d_y*i, x_start+d_x*i, length, d_y, d_x):

            state = is_bounded(board, y_start + d_y * i + d_y * (length-1),
                               x_start+d_x*i + d_x*(length-1), length, d_y, d_x)
            if state == "CLOSED":
                closed_seq_count += 1

    return closed_seq_count


def detect_rows_closed_5(board, col, length):
    closed_rows_5 = 0

    # checking columns:
    for i in range(len(board[0])):
        res = detect_row_closed(board, col, 0, i, 5, 1, 0)
        closed_rows_5 += res

    for i in range(len(board)):

        res = detect_row_closed(board, col, i, 0, 5, 0, 1)
        closed_rows_5 += res

    for i in range(len(board)-2):
        if is_sq_in_board(board, 0+1*5, i+1*5):
            res = detect_row_closed(board, col, 0, i, 5, 1, 1)
            closed_rows_5 += res

    for i in range(1, len(board)-2):
        if is_sq_in_board(board, i+1*5, 0+1*5):
            res = detect_row_closed(board, col, i, 0, 5, 1, 1)
            closed_rows_5 += res

    for i in range(2, len(board)-1):
        if is_sq_in_board(board, 0+1*5, i+1*-5):

            res = detect_row_closed(board, col, 0, i, 5, 1, -1)
            closed_rows_5 += res

    for i in range(0, len(board)-2):
        if is_sq_in_board(board, i+1*5, 0-1*5):
            res = detect_row_closed(board, col, i, 7, 5, 1, -1)
            closed_rows_5 += res

    return closed_rows_5


# four ways a row can be achieved
# 1. dy = 1, dx = 0 column
# 2. dy = 0, dx = 1 row
# 3. dy = 1, dx = 1 diagonal (top left to bottom right)
# 4. dy = 1, dx = -1 diagonal (top right to bottom left)


# strategy: check every column first -> for loop, calling detect_row each instance
#           check every row -> for loop
#           diagonal (TL to BR) -> check starting at (5, 0) to (0, 5) ## might have to change since need 5 for a win
#           diagonal (TR to BL) -> check starting at (5, 7) to (2, 2)

def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0

    # checking columns:
    for i in range(len(board[0])):
        res = detect_row(board, col, 0, i, length, 1, 0)
        open_seq_count += res[0]
        semi_open_seq_count += res[1]

    for i in range(len(board)):
        res = detect_row(board, col, i, 0, length, 0, 1)
        open_seq_count += res[0]
        semi_open_seq_count += res[1]

    for i in range(len(board)-2):
        res = detect_row(board, col, 0, i, length, 1, 1)
        open_seq_count += res[0]
        semi_open_seq_count += res[1]

    for i in range(1, len(board)-2):
        res = detect_row(board, col, i, 0, length, 1, 1)
        open_seq_count += res[0]
        semi_open_seq_count += res[1]

    for i in range(2, len(board)-1):
        res = detect_row(board, col, 0, i, length, 1, -1)
        open_seq_count += res[0]
        semi_open_seq_count += res[1]

    for i in range(0, len(board)-2):
        res = detect_row(board, col, i, 7, length, 1, -1)
        open_seq_count += res[0]
        semi_open_seq_count += res[1]

    return open_seq_count, semi_open_seq_count


def search_max(board):
    # strategy, go through every empty square, row by row, 'place' a black stone in every instace
    # call the score function, store highest values in an empty list, have a another list with
    # the coordinates of the respective score. After, index the score list to find the max, find the correspdnding coords
    scores = []
    coords = []
    max_score_index = 0
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] != " ":  # already a stone
                pass

            else:
                board[y][x] = "b"
                scores.append(score(board))
                coords.append([y, x])
                board[y][x] = " "
    if len(scores) == 0:  # nothing could be played
        return "Draw"
    max_score_index = scores.index(max(scores))
    move_y = coords[max_score_index][0]
    move_x = coords[max_score_index][1]

    return move_y, move_x


def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4]) +
            500 * open_b[4] +
            50 * semi_open_b[4] +
            -100 * open_w[3] +
            -30 * semi_open_w[3] +
            50 * open_b[3] +
            10 * semi_open_b[3] +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win(board):
    # This function determines the current status of the game, and returns one of
    # ["White won", "Black won", "Draw", "Continue playing"], depending on the current status
    # on the board. The only situation where "Draw" is returned is when board is full.

    # strategy: white or black only wins when max_score is either 100000 for black and -100000 for white
    # for Draw: if search_max == "DRAW"
    # Else continue playing
    if score(board) == -100000 or detect_rows_closed_5(board, "w", 5) >= 1:
        return "White won"
    elif score(board) == 100000 or detect_rows_closed_5(board, "b", 5) >= 1:
        return "Black won"
    elif search_max(board) == "Draw":
        return "Draw"
    else:
        return "Continue playing"


def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i % 10) + "|"
    s += str((len(board[0])-1) % 10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i % 10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i)
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))


def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res


def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


board = make_empty_board(8)

board = [[' ', ' ', 'w', ' ', ' ', ' ', ' ', ' '], [' ', 'w', ' ', ' ', 'w', ' ', ' ', ' '], ['w', ' ', ' ', ' ', 'w', ' ', ' ', ' '], [' ', ' ', ' ',
                                                                                                                                        ' ', ' ', ' ', ' ', 'w'], ['w', ' ', 'w', ' ', 'w', 'w', 'w', 'w'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['w', 'w', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', 'w', ' ', ' ', 'w', ' ', ' ']]
print_board(board)
print(is_win(board))

print(detect_rows_closed_5(board, 'w', 5))


# board = [[' ', ' ', 'w', ' ', ' ', 'w', ' ', ' '], [' ', 'w', ' ', ' ', 'w', ' ', ' ', ' '], ['w', 'w', ' ', ' ', 'w', ' ', ' ', ' '], [' ', ' ', ' ', ' ', ' ', 'w', 'w', 'w'], ['w', ' ', 'w', ' ', 'w', 'w', 'w', 'w'], [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '], ['w', 'w', ' ', ' ', ' ', ' ', ' ', ' '], [' ', ' ', 'w', ' ', ' ', 'w', ' ', ' ']]
