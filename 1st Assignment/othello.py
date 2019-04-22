from random import randint


def print_board(board, score):  # print the current board status
    print("   A   B  C  D   E   F  G  H")
    for i in range(8):
        print("%i [" % (i + 1), end="")
        for j in range(7):
            print(board[i][j], end="][")
        print('%s]' % board[i][7])
    print("Score: Black %i - White %i" % (score[0], score[1]))


def play_permit(board, color, coordinates, score):  # check if a movement can be made
    y, x = coordinates
    if color == black:
        opponentColor = white
    else:
        opponentColor = black
    if -1 < x < 8 and -1 < y < 8:  # checking if the coordinates exist
        if board[y][x] == color or board[y][x] == opponentColor:
            print("occupied block")
            return False
        y1 = y - 1  # y position of the top left square on the board
        x1 = x - 1  # x position of the top left square on the board
        # print("checking %i %i, color is %s" % (y1 , x1, board[y1][x1]))
        flag = False
        for i in range(3):  # going through all neighbor squares (if they exist)
            y1 += i
            # print("checking %i %i, color is %s" % (y1, x1, board[y1][x1]))
            for j in range(3):
                if -1 < x1 + j < 8 and -1 < y1 + i < 8:
                    if board[y1][x1 + j] == opponentColor:  # if a neighbor square belongs to the opponent:
                        dx = x1 + j - x  # if we must look for blocks in the x axis this value will be 1 or -1
                        dy = y1 - y  # if we must move on the y axis as well, this value will be 1 or -1
                        # these combinations allow us to move in every direction we need
                        x2 = x1 + j + dx  # new x position of the square we have to check
                        y2 = y1 + dy  # new y position of the square we have to check
                        while True:
                            if 8 < x2 or x2 < 0 or 8 < y2 or y2 < 0:  # if we reach the end of the board we stop
                                break
                            # print("checking %i %i, color is %s" % (y2, x2, board[y2][x2]))
                            if board[y2][x2] == color:  # if True, user's input is a valid position, so we begin
                                # flipping the disks
                                flag = True
                                dx *= -1  # we now need to move to the opposite direction
                                dy *= -1
                                y2 += dy
                                x2 += dx
                                while board[y2][x2] == opponentColor:
                                    board[y2][x2] = color  # flipping disks
                                    y2 += dy
                                    x2 += dx
                                    if opponentColor == black:
                                        score[0] -= 1
                                        score[1] += 1
                                    else:
                                        score[0] += 1
                                        score[1] -= 1
                                board[y][x] = color  # placing a new disk in the square selected by the user
                                break
                            y2 += dy
                            x2 += dx

        return flag
    else:
        print("Invalid move")
        return False


black = u"\u25CF"  # unicode for black disks
white = u"\u25CB"  # unicode for white/transparent disks
empty = u"\u203F"  # unicode for underscore
score = [2, 2]
board = [[empty for x in range(8)] for y in range(8)]
board[3][3] = board[4][4] = white
board[4][3] = board[3][4] = black
turn = 1
print("Welcome to Othello.\nPress 'B' for black, 'W' for white, or any other button for random")
response = input().lower()
if response != 'b' and response != 'w':
    response = randint(0, 1)
    if response == 0:
        response = 'b'
    else:
        response = 'w'
if response == 'b':
    print("You play first")
    turn = 1
elif response == 'w':
    print("PC plays first")
    turn = 2
print_board(board, score)
turnCounter = 0
while turnCounter < 60:
    if turn % 2 == 1:
        flag = False
        while not flag:
            print("Please enter the coordinates : ")
            response = input().upper()
            line = int(response[0]) - 1
            column = ord(response[1]) - 65
            flag = play_permit(board, black, (line, column), score)
        print_board(board, score)

    else:
        print("PC plays here")
    turn += 1
