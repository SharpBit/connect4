import numpy as np
import random 
import math
from connect4 import Board
# 1 is AI 2 is ENEMY

b2 = np.zeros((6,7))

b2[5][0] = 1
b2[5][1] = 2
b2[5][2] = 1
b2[5][3] = 1
b2[5][4] = 1
b2[5][5] = 2
b2[5][6] = 1

b2[4][0] = 1
b2[4][1] = 2
b2[4][2] = 1
b2[4][3] = 1
b2[4][4] = 1
b2[4][5] = 2
b2[4][6] = 1

b2[3][0] = 2
b2[3][1] = 1
b2[3][2] = 2
b2[3][3] = 1
b2[3][4] = 2
b2[3][5] = 1
b2[3][6] = 2

b2[2][0] = 2
b2[2][1] = 1
b2[2][2] = 2
b2[2][3] = 1
b2[2][4] = 2
b2[2][5] = 1
b2[2][6] = 2

b2[1][0] = 0
b2[1][1] = 0
b2[1][2] = 0
b2[1][3] = 0
b2[1][4] = 0
b2[1][5] = 0
b2[1][6] = 0

print(b2)

game_over = 1

def get_open_row(board, col):
    for r in range(len(board)):
        if board[r][col] == 0:
            row = r
    return row

def max_score_move(bd):
    '''
    for the 6 open spots, this function calculates which one has the greatest score
    if the max scores are the same, the move is randomized (BETWEEN THE AMOUNT OF MAX SCORES )
    PS. IF THERE ARE MULTIPLE MAX SCORES THE PIECE WILL BE PLACED IN THE RIGHTMOST MAX COLUMN
    I COULD NOT FIGURE OUT HOW TO RANDOMIZE A POSITION WITHIN THE MAX SCORES
    '''

    # Now we get the max score of each one of those locations
    # Meaning: for each location we test the score they would be in every direction and
    # the max score will be saved as the "score" for that location

    max_score = 0
    best_move = 3  # default to the center
    for col in range(7):
        # move = (bd.Board.first_empty[col], col)                           
        move = (get_open_row(bd,col),col) #fist empty not working idk why so I switched to get_open_row
        print('SCORE 0 ------------------------------------------')
        score = 0

        # going down
        print('down')
        # move[0] is the number of rows below the current row
        # For example, there are 0 rows below row 0
        # Since the end bound of range() is exclusive, we add 1
        for dr in range(1, min(move[0] + 1, 4)):
            if bd.get_position(move[0] - dr, move[1]) == bd.PLAYER_TWO:
                # blocked in this direction by opponent, break
                break
            if bd.get_position(move[0] - dr, move[1]) == bd.PLAYER_ONE:
                print('score+2')
                score += 2
                if score >= 6:
                    print('WINN')
                    return move[1]  # if this score is reached at any point in the game, this move should be made

        if score > max_score:
            max_score = score
            best_move = move[1]

        # going right
        score = 0
        print('right')
        # bd.COLs - move[1] - 1 is the number of rows to the right of the current col
        # For example, there are 0 rows to the right of col 6 (7 - 6 - 1 = 0)
        # Since the end bound of range() is exclusive, we add 1, cancelling out the -1
        for dc in range(1, min(bd.COLS - move[1], 4)):
            if bd.get_position(move[0], move[1] + dc) == bd.PLAYER_TWO:
                break
            elif bd.get_position(move[0], move[1] + dc) == bd.PLAYER_ONE:
                print('score+2')
                score += 2
                if score >= 6:
                    print('WINN')
                    return col  # if this score is reached at any point in the game, this move should be made

        # going left
        print('left')
        # move[1] is the number of rows to the left of the current col
        # For example, there are 0 rows to the right of col 0
        # Since the end bound of range() is exclusive, we add 1
        for dc in range(1, min(move[1] + 1, 4)):
            if bd.get_position(move[0], move[1] - dc) == 2:
                break
            elif bd.get_position(move[0], move[1] - dc) == 1:
                print('score+2')
                score += 2
                if score >= 6:
                    print('WINN')
                    return col  # if this score is reached at any point in the game, this move should be made

        if score > max_score:
            max_score = score
            best_move = move[1]
        score = 0

        # going down right
        print('down right')
        for diag_offset in range(1, min(move[0] + 1, bd.COLS - move[1], 4)):
            if bd.get_position(move[0] - diag_offset, move[1] + diag_offset) == bd.PLAYER_TWO:
                break
            elif bd.get_position(move[0] - diag_offset, move[1] + diag_offset) == 1:
                print('score+2')
                score += 2
                if score >= 6:
                    print('WINN')
                    return move[1]

        # up left
        print('up left')
        for diag_offset in range(1, min(move[1] + 1, bd.ROWS - move[0], 4)):
            if bd.get_position(move[0] + diag_offset, move[1] - diag_offset) == bd.PLAYER_TWO:
                break
            elif bd.get_position(move[0] + diag_offset, move[1] - diag_offset) == 1:
                print('score+2')
                score += 2
                if score >= 6:
                    print('WINN')
                    return move[1]

        # reseting scores
        if score > max_score:
            max_score = score
            best_move = move[1]
        score = 0

        # down left
        print('down left')
        for diag_offset in range(1, min(4, move[1]+1, bd.COLUMNS-move[1])):
            if bd.get_position(move[0] - diag_offset, move[1] - diag_offset) == bd.PLAYER_TWO:
                break
            elif bd.get_position(move[0] - diag_offset, move[1] - diag_offset) == 1:
                print('score+2')
                score += 2
                if score >= 6:
                    print('WINN')
                    return move[1]

        # up right
        print('up right')
        for diag_offset in range(1, min(4,bd.COLUMNS-move[1],bd.ROWS-move[0])):
            if bd.get_position(move[0] + diag_offset, move[1] + diag_offset) == bd.PLAYER_TWO:
                break
            elif bd.get_position(move[0] + diag_offset, move[1] + diag_offset) == 1:
                print('score+2')
                score += 2
                if score >= 6:
                    print('WINN')
                    return move[1]


        # reseting scores
        if score > max_score:
            max_score = score
            best_move = move[1]
        score = 0


    return best_move



while game_over <= 1: 
    # this will be 
    # while game_over == False 
    # but for now just run it a few times
    col = max_score_move(b2)

    # best_position = ( get_open_row(b3,col) ,  col    )
    # print('BEST MOVE ------------------------>',best_position)
    # b2[best_position[0]][best_position[1]] = 2

    game_over += 1

