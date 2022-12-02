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
        target = None
        scores = [0, 0]  # [AI score, opponent score]

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
            piece = bd.get_position(move[0] - dr, move[1])
            if not target and piece == bd.EMPTY:
                continue
            if not target:
                target = piece
            if piece == target:
                scores[target - 1] += 1
                if scores[0] >= 3 or scores[1] >= 3:
                    # either we win or we block a winning spot
                    return move[1]
            elif piece != bd.EMPTY:  # opponent piece
                break

        print(f'down {scores=}')
        # resetting scores
        if scores[0] > max_score:
            max_score = scores[0]
            best_move = move[1]
        target = None
        scores = [0, 0]

        # going left
        for dc in range(1, min(cols_left, 4)):
            piece = bd.get_position(move[0], move[1] - dc)
            if not target and piece == bd.EMPTY:
                continue
            if not target:
                target = piece
            if piece == target:
                scores[target - 1] += 1
                if scores[0] >= 3 or scores[1] >= 3:
                    # either we win or we block a winning spot
                    return move[1]
            elif piece != bd.EMPTY:  # opponent piece
                break

        target = None
        # going right
        for dc in range(1, min(cols_right, 4)):
            piece = bd.get_position(move[0], move[1] + dc)
            if not target and piece == bd.EMPTY:
                continue
            if not target:
                target = piece
            if piece == target:
                scores[target - 1] += 1
                if scores[0] >= 3 or scores[1] >= 3:
                    # either we win or we block a winning spot
                    return move[1]
            elif piece != bd.EMPTY:  # opponent piece
                break

        print(f'left/right {scores=}')
        # resetting scores
        if scores[0] > max_score:
            max_score = scores[0]
            best_move = move[1]
        target = None
        scores = [0, 0]

        # going down right
        for diag_offset in range(1, min(rows_below, cols_right, 4)):
            piece = bd.get_position(move[0] - diag_offset, move[1] + diag_offset)
            if not target and piece == bd.EMPTY:
                continue
            if not target:
                target = piece
            if piece == target:
                scores[target - 1] += 1
                if scores[0] >= 3 or scores[1] >= 3:
                    # either we win or we block a winning spot
                    return move[1]
            elif piece != bd.EMPTY:  # opponent piece
                break

        target = None
        # up left
        for diag_offset in range(1, min(rows_above, cols_left, 4)):
            piece = bd.get_position(move[0] + diag_offset, move[1] - diag_offset)
            if not target and piece == bd.EMPTY:
                continue
            if not target:
                target = piece
            if piece == target:
                scores[target - 1] += 1
                if scores[0] >= 3 or scores[1] >= 3:
                    # either we win or we block a winning spot
                    return move[1]
            elif piece != bd.EMPTY:  # opponent piece
                break

        print(f'down right/up left {scores=}')
        # resetting scores
        if scores[0] > max_score:
            max_score = scores[0]
            best_move = move[1]
        target = None
        scores = [0, 0]

        # down left
        for diag_offset in range(1, min(rows_below, cols_left, 4)):
            piece = bd.get_position(move[0] - diag_offset, move[1] - diag_offset)
            if not target and piece == bd.EMPTY:
                continue
            if not target:
                target = piece
            if piece == target:
                scores[target - 1] += 1
                if scores[0] >= 3 or scores[1] >= 3:
                    # either we win or we block a winning spot
                    return move[1]
            elif piece != bd.EMPTY:  # opponent piece
                break

        target = None
        # up right
        for diag_offset in range(1, min(rows_above, cols_right, 4)):
            piece = bd.get_position(move[0] + diag_offset, move[1] + diag_offset)
            if not target and piece == bd.EMPTY:
                continue
            if not target:
                target = piece
            if piece == target:
                scores[target - 1] += 1
                if scores[0] >= 3 or scores[1] >= 3:
                    # either we win or we block a winning spot
                    return move[1]
            elif piece != bd.EMPTY:  # opponent piece
                break

        print(f'down left/up right {scores=}')
        # resetting scores
        if scores[0] > max_score:
            max_score = scores[0]
            best_move = move[1]
        print(f'{col=} {max_score=} {best_move=}\n')

    return best_move
