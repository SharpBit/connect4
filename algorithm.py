def get_best_move(bd):
    '''
    For the 7 open spots, this function calculates which one has the greatest score
    if the max scores are the same, the move is randomized (BETWEEN THE AMOUNT OF MAX SCORES )
    PS. IF THERE ARE MULTIPLE MAX SCORES THE PIECE WILL BE PLACED IN THE RIGHTMOST MAX COLUMN
    I COULD NOT FIGURE OUT HOW TO RANDOMIZE A POSITION WITHIN THE MAX SCORES
    '''

    # Now we get the max score of each one of those locations
    # Meaning: for each location we test the score they would be in every direction and
    # the max score will be saved as the "score" for that location

    max_score = 0
    best_move = 3  # default to the center column
    for col in range(7):
        move = (bd.first_empty[col], col)

        if bd.is_col_full(move[0]):  # Col is full, skip
            continue
        print('COLUMN:', col)
        score = 0

        # move[0] is the number of rows below the current row
        # For example, there are 0 rows below row 0
        # Since the end bound of range() is exclusive, we add 1
        rows_below = move[0] + 1
        # bd.ROWS - move[0] - 1 is the number of rows above the current row
        # For example, there are 0 rows above row 5 (6 - 5 - 1 = 0)
        # Since the end bound of range() is exclusive, we add 1, cancelling out the -1
        rows_above = bd.ROWS - move[0]
        # move[1] is the number of rows to the left of the current col
        # For example, there are 0 rows to the right of col 0
        # Since the end bound of range() is exclusive, we add 1
        cols_left = move[1] + 1
        # bd.COLS - move[1] - 1 is the number of rows to the right of the current col
        # For example, there are 0 rows to the right of col 6 (7 - 6 - 1 = 0)
        # Since the end bound of range() is exclusive, we add 1, cancelling out the -1
        cols_right = bd.COLS - move[1]

        # going down
        for dr in range(1, min(rows_below, 4)):
            if bd.get_position(move[0] - dr, move[1]) == bd.PLAYER_TWO:
                # blocked in this direction by opponent, break
                break
            if bd.get_position(move[0] - dr, move[1]) == bd.PLAYER_ONE:
                score += 1
                if score >= 3:
                    return move[1]  # if this score is reached at any point in the game, this move should be made

        print(f'down {score=}')
        # resetting scores
        if score > max_score:
            max_score = score
            best_move = move[1]
        score = 0

        # going left
        for dc in range(1, min(cols_left, 4)):
            if bd.get_position(move[0], move[1] - dc) == bd.PLAYER_TWO:
                break
            elif bd.get_position(move[0], move[1] - dc) == bd.PLAYER_ONE:
                score += 1
                if score >= 3:
                    return move[1]  # if this score is reached at any point in the game, this move should be made

        # going right
        for dc in range(1, min(cols_right, 4)):
            if bd.get_position(move[0], move[1] + dc) == bd.PLAYER_TWO:
                break
            elif bd.get_position(move[0], move[1] + dc) == bd.PLAYER_ONE:
                score += 1
                if score >= 3:
                    return move[1]  # if this score is reached at any point in the game, this move should be made

        print(f'left/right {score=}')
        # resetting scores
        if score > max_score:
            max_score = score
            best_move = move[1]
        score = 0

        # going down right
        for diag_offset in range(1, min(rows_below, cols_right, 4)):
            if bd.get_position(move[0] - diag_offset, move[1] + diag_offset) == bd.PLAYER_TWO:
                break
            elif bd.get_position(move[0] - diag_offset, move[1] + diag_offset) == bd.PLAYER_ONE:
                score += 1
                if score >= 3:
                    return move[1]

        # up left
        for diag_offset in range(1, min(rows_above, cols_left, 4)):
            if bd.get_position(move[0] + diag_offset, move[1] - diag_offset) == bd.PLAYER_TWO:
                break
            elif bd.get_position(move[0] + diag_offset, move[1] - diag_offset) == bd.PLAYER_ONE:
                score += 1
                if score >= 3:
                    return move[1]

        print(f'down right/up left {score=}')
        # resetting scores
        if score > max_score:
            max_score = score
            best_move = move[1]
        score = 0

        # down left
        for diag_offset in range(1, min(rows_below, cols_left, 4)):
            if bd.get_position(move[0] - diag_offset, move[1] - diag_offset) == bd.PLAYER_TWO:
                break
            elif bd.get_position(move[0] - diag_offset, move[1] - diag_offset) == bd.PLAYER_ONE:
                score += 1
                if score >= 3:
                    return move[1]

        # up right
        for diag_offset in range(1, min(rows_above, cols_right, 4)):
            if bd.get_position(move[0] + diag_offset, move[1] + diag_offset) == bd.PLAYER_TWO:
                break
            elif bd.get_position(move[0] + diag_offset, move[1] + diag_offset) == bd.PLAYER_ONE:
                score += 1
                if score >= 3:
                    return move[1]

        print(f'down left/up right {score=}')
        # resetting scores
        if score > max_score:
            max_score = score
            best_move = move[1]
        print(f'{col=} {max_score=} {best_move=}\n')

    return best_move
