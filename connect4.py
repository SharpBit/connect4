import argparse
import asyncio
import websockets

from algorithm import get_best_move
from typing import Tuple


OUTCOME_RESPS = ('WIN', 'LOSS', 'DRAW')


class Board:
    EMPTY = 0
    PLAYER_ONE = 1
    PLAYER_TWO = 2
    ROWS = 6
    COLS = 7

    def __init__(self):
        # 7x6 representation with self.grid[col][0] representing the bottom row of each col
        # and self.grid[col][5] representing the top row of each col
        self.grid = [[self.EMPTY] * self.ROWS for _ in range(self.COLS)]
        self.first_empty = [0 for _ in range(self.COLS)]

    def insert(self, player: int, col: int):
        self.grid[col][self.first_empty[col]] = player
        self.first_empty[col] += 1

    def get_position(self, row: int, col: int) -> int:
        '''Gets the space at a specific row and column'''
        print(row, col)
        return self.grid[col][row]  # accessed by [col][row]

    def is_col_full(self, col: int) -> bool:
        '''Returns whether or not a column is full'''
        return col >= self.ROWS  # Row 6 or higher (col is full)

    def __str__(self) -> str:
        rows = len(self.grid[0])
        cols = len(self.grid)
        res = ''
        for r in range(rows - 1, -1, -1):
            for c in range(cols):
                res += str(self.grid[c][r])
                res += '\n' if c == cols - 1 else ' '
        return res


async def ask_move(websocket, board: Board, human=False, wait_ms=1000) -> Tuple[Tuple, int]:
    resp = ('OK',)
    move = None
    while resp[0] != 'ACK':
        if resp[0] == 'ERROR':
            print(resp)
        elif resp[0] in OUTCOME_RESPS:
            return resp, move

        if human:  # For debugging purposes
            move = int(input('Enter a column: '))
        else:
            if wait_ms:
                await asyncio.sleep(wait_ms / 1000)
            move = get_best_move(board)
        await websocket.send(f'PLAY:{move}')
        resp = tuple((await websocket.recv()).split(':'))
    return resp, move

async def create_game(server_ip='localhost', human=False, wait_ms=1000):
    async with websockets.connect(f'ws://{server_ip}:5000/create') as websocket:
        board = Board()
        while True:
            resp = tuple((await websocket.recv()).split(':'))
            print(resp)
            if resp[0] == 'GAMESTART':
                _, move = await ask_move(websocket, board, human=human, wait_ms=wait_ms)
                board.insert(Board.PLAYER_ONE, move)
                print(board)
            elif resp[0] == 'OPPONENT':
                board.insert(Board.PLAYER_TWO, int(resp[1]))
                print(board)
                resp, move = await ask_move(websocket, board, human=human)
                if move is not None and resp[0] not in OUTCOME_RESPS:
                    board.insert(Board.PLAYER_ONE, move)
                    print(board)
            if resp[0] in OUTCOME_RESPS:
                print(resp[0])
                break

async def join_game(game_id, server_ip='localhost', human=False, wait_ms=1000):
    async with websockets.connect(f'ws://{server_ip}:5000/join/{game_id}') as websocket:
        board = Board()
        while True:
            resp = tuple((await websocket.recv()).split(':'))
            print(resp)
            if resp[0] == 'OPPONENT':
                board.insert(Board.PLAYER_TWO, int(resp[1]))
                print(board)
                resp, move = await ask_move(websocket, board, human=human, wait_ms=wait_ms)
                if resp[0] in OUTCOME_RESPS:
                    print(resp[0])
                    break
                board.insert(Board.PLAYER_ONE, move)
                print(board)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create', action='store_true', help='Create a game.')
    parser.add_argument('-j', '--join', help='Join a game using the game ID.')
    parser.add_argument('--server_ip', default='localhost', help='The server IP to connect to (defaults to localhost)')
    parser.add_argument('--human', action='store_true', help='Play as a human.')
    parser.add_argument('--wait', type=int, default=1000, help='# milliseconds to wait before making a move as an AI.')
    args = parser.parse_args()

    if args.create and args.join:
        print('Cannot both create and join a game.')
        parser.print_help()
    elif args.create:
        asyncio.run(create_game(server_ip=args.server_ip, human=args.human, wait_ms=args.wait))
    elif args.join:
        asyncio.run(join_game(args.join, server_ip=args.server_ip, human=args.human, wait_ms=args.wait))
    else:
        parser.print_help()
