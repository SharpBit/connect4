from typing import Tuple


def get_best_move(bd) -> int:
    '''
    For the 7 open spots, this function calculates which one has the greatest score
    if the max scores are the same, the leftmost move is made. If an enemy has a winning move,
    block that spot.
    '''

    max_score = 0
    best_move = 3  # default to the center column
    for col in range(bd.COLS):
        move = (bd.first_empty[col], col)

        if bd.is_col_full(move[0]):  # Col is full, skip
            continue
        print('COLUMN:', col)
        scores = [0, 0]  # [AI score, opponent score]

        dists_to_edge = {}
        # move[0] is the number of rows below the current row
        # For example, there are 0 rows below row 0
        # Since the end bound of range() is exclusive, we add 1
        dists_to_edge[(-1, 0)] = move[0] + 1
        # bd.ROWS - move[0] - 1 is the number of rows above the current row
        # For example, there are 0 rows above row 5 (6 - 5 - 1 = 0)
        # Since the end bound of range() is exclusive, we add 1, cancelling out the -1
        dists_to_edge[(1, 0)] = bd.ROWS - move[0]
        # move[1] is the number of rows to the left of the current col
        # For example, there are 0 rows to the right of col 0
        # Since the end bound of range() is exclusive, we add 1
        dists_to_edge[(0, -1)] = move[1] + 1
        # bd.COLS - move[1] - 1 is the number of rows to the right of the current col
        # For example, there are 0 rows to the right of col 6 (7 - 6 - 1 = 0)
        # Since the end bound of range() is exclusive, we add 1, cancelling out the -1
        dists_to_edge[(0, 1)] = bd.COLS - move[1]

        def check_dir(direction: Tuple[int, int], board) -> bool:
            target = None
            dists_to_check = [4]
            if direction[0] != 0:
                dists_to_check.append(dists_to_edge[(direction[0], 0)])
            if direction[1] != 0:
                dists_to_check.append(dists_to_edge[(0, direction[1])])

            for offset in range(1, min(dists_to_check)):
                # don't need to declare move as nonlocal since we are not reassigning
                piece = board.get_position(move[0] + offset * direction[0], move[1] + offset * direction[1])
                if target is None and piece == board.EMPTY:
                    continue
                if target is None:
                    target = piece
                if piece == target:
                    # don't need to declare scores as nonlocal since we are modifying, not reassigning
                    scores[target - 1] += 1
                    if scores[0] >= 3 or scores[1] >= 3:
                        # either we win or we block a winning spot
                        return True
                elif piece != board.EMPTY:  # opponent piece
                    break

            # It's fine to update scores for each direction and not each axis
            # since if the score increases in the other direction on the same axis later,
            # the score will update and reflect that
            nonlocal max_score
            nonlocal best_move
            if scores[0] > max_score:
                max_score = scores[0]
                best_move = move[1]
            return False

        # going down
        if check_dir((-1, 0), bd):
            return move[1]
        print(f'down {scores=}')
        scores = [0, 0]

        # going left
        if check_dir((0, -1), bd):
            return move[1]
        # going right
        if check_dir((0, 1), bd):
            return move[1]
        print(f'left/right {scores=}')
        scores = [0, 0]

        # down right
        if check_dir((-1, 1), bd):
            return move[1]
        # up left
        if check_dir((1, -1), bd):
            return move[1]
        print(f'down right/up left {scores=}')
        scores = [0, 0]

        # down left
        if check_dir((-1, -1), bd):
            return move[1]
        # up right
        if check_dir((1, 1), bd):
            return move[1]
        print(f'down left/up right {scores=}')

        print(f'{col=} {max_score=} {best_move=}\n')

    return best_move
