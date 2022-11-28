import numpy as np
import random 
import math

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

    # First we get the exact locations of the 6 possible moves (0-5)
    move0 = (get_open_row(bd,0) ,0) 
    move1 = (get_open_row(bd,1) ,1)
    move2 = (get_open_row(bd,2) ,2)
    move3 = (get_open_row(bd,3) ,3)
    move4 = (get_open_row(bd,4) ,4)
    move5 = (get_open_row(bd,5) ,5)
    move6 = (get_open_row(bd,6) ,6)

    # Now we get the max score of each one of those locations
    # Meaning: for each location we test the score they would be in every direction and 
    # the max score will be saved as the "score" for that location
    

    print('SCORE 1 ------------------------------------------')

    #SCORE 0
    score0 = 0 

    #going down
    for i in range(1, len(bd)- get_open_row(bd,0)):
        print(i)
        if bd[move0[0] +i][0] == 2:
            break
        elif bd[move0[0] +i][0] == 1:
            print('score+2')
            score0 += 2
            if score0 == 6:
                return 0 # if this score is reached at any point in the game, this move should be made


    #going right
    # for i in range(1, len(bd[get_open_row(bd,0)]) - 0): --> WORNG RANGE BUT KINDA WORDS likely worse implementation 
    for i in range(1, 4):
        print(i)
        if bd[move0[0]][0+i] == 2:
            break
        elif bd[get_open_row(bd,0)] [ move0[1] + i] == 1:
            print('score+2')
            score0 += 2
            if score0 == 6:
                return 0 # if this score is reached at any point in the game, this move should be made

    #going down right
    for i in range(1, min(4,(4-move0[0]))):
        print(i)
        if bd[move0[0]+i][0+i] == 2:
            break
        elif bd[move0[0]+i][0+i] == 1:
            print('score+2')
            score0 += 2
            if score0 == 6:
                return 0


    #SCORE 1 

    #SCORE 2

    #SCORE 3

    #SCORE 4

    #SCORE 5

    print('SCORE 6 ------------------------------------------')

    #SCORE 6
    score6 = 0 

    #going down
    for i in range(1, len(bd)- get_open_row(bd,6)):
        print(i)
        if bd[move6[0] +i][0] == 2:
            break
        elif bd[move6[0] +i][0] == 1:
            print('score+2')
            score6 += 2
            if score6 == 6:
                return 6 # if this score is reached at any point in the game, this move should be made


    #going left
    # for i in range(1, len(bd[get_open_row(bd,0)]) - 0): --> WORNG RANGE BUT KINDA WORDS likely worse implementation 
    for i in range(1, 4):
        print(i)
        if bd[move6[0]][0-i] == 2:
            break
        elif bd[get_open_row(bd,0)] [ move6[1] - i] == 1:
            print('score+2')
            score5 += 2
            if score5 == 6:
                return 6 # if this score is reached at any point in the game, this move should be made

    for i in range(1, min(4,(4-move5[0]))):
        print(i)
        if bd[move5[0]+i][0+i] == 2:
            break
        elif bd[move5[0]+i][0+i] == 1:
            print('score+2')
            score5 += 2
            if score5 == 6:
                return 6


    



    return None



while game_over <= 1: 
    # this will be 
    # while game_over == False 
    # but for now just run it a few times
    col = max_score_move(b2)

    # best_position = ( get_open_row(b3,col) ,  col    )
    # print('BEST MOVE ------------------------>',best_position)
    # b2[best_position[0]][best_position[1]] = 2

    game_over += 1

