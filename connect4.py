import argparse
import asyncio
from AIbestColumn import minimax
import websockets
import math

from typing import Tuple


class Board:
    EMPTY = 0
    PLAYER_ONE = 1
    PLAYER_TWO = 2

    def __init__(self):
        # 7x6 representation with self.grid[col][0] representing the bottom row of each col
        # and self.grid[col][5] representing the top row of each col
        self.grid = [[self.EMPTY] * 6 for _ in range(7)]
        self.first_empty = [0 for _ in range(7)]

    def insert(self, player: int, col: int):
        self.grid[col][self.first_empty[col]] = player
        self.first_empty[col] += 1

    def get_position(self, row, col):
        return self.grid[row][col]

    def __str__(self):
        rows = len(self.grid[0])
        cols = len(self.grid)
        res = ''
        for r in range(rows - 1, -1, -1):
            for c in range(cols):
                res += str(self.grid[c][r])
                res += '\n' if c == cols - 1 else ' '
        return res

# def get_score(bd):
#     return None


async def ask_move(websocket,board) -> Tuple[Tuple, int]:
    resp = ('OK',)
    move = None
    while resp[0] != 'ACK':
        if resp[0] == 'ERROR':
            print(resp)
        elif resp[0] in ('WIN', 'DRAW', 'LOSS'):
            return resp, move

        move = minimax(board, 5, -math.inf, math.inf, True)[0] #REPLACE THIS WITH FUNCTION make sure returns int between 0-6
        
        await websocket.send(f'PLAY:{move}')
        resp = tuple((await websocket.recv()).split(':'))
    return resp, move

async def create_game(server_ip='localhost'):
    async with websockets.connect(f'ws://{server_ip}:5000/create') as websocket:
        board = Board()
        while True:
            resp = tuple((await websocket.recv()).split(':'))
            print(resp)
            if resp[0] == 'GAMESTART':
                _, move = await ask_move(websocket)
                board.insert(Board.PLAYER_ONE, move)
                print(board)
            elif resp[0] == 'OPPONENT':
                board.insert(Board.PLAYER_TWO, int(resp[1]))
                print(board)
                resp, move = await ask_move(websocket,board)
                if move is not None:
                    board.insert(Board.PLAYER_ONE, move)
                    print(board)
            if resp[0] in ('WIN', 'LOSS', 'DRAW'):
                print(resp[0])
                break

async def join_game(game_id, server_ip='localhost'):
    async with websockets.connect(f'ws://{server_ip}:5000/join/{game_id}') as websocket:
        board = Board()
        while True:
            resp = tuple((await websocket.recv()).split(':'))
            print(resp)
            if resp[0] == 'OPPONENT':
                board.insert(Board.PLAYER_TWO, int(resp[1]))
                print(board)
                resp, move = await ask_move(websocket,board)
                if resp[0] in ('WIN', 'LOSS', 'DRAW'):
                    print(resp[0])
                    break
                board.insert(Board.PLAYER_ONE, move)
                print(board)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--create', action='store_true', help='Create a game.')
    parser.add_argument('-j', '--join', help='Join a game using the game ID.')
    parser.add_argument('--server_ip', default='localhost', help='The server IP to connect to (defaults to localhost)')
    args = parser.parse_args()

    if args.create and args.join:
        print('Cannot both create and join a game.')
        parser.print_help()
    elif args.create:
        asyncio.run(create_game())
    elif args.join:
        asyncio.run(join_game(args.join))
    else:
        parser.print_help()
