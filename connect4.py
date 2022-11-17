import asyncio
import websockets
# import random
import sys

async def create_game():
    async with websockets.connect('ws://localhost:5000/create') as websocket:
        while True:
            resp = await websocket.recv()
            print(resp)
            if resp == 'GAMESTART' or resp.startswith('OPPONENT'):
                move = int(input('Column: '))
                await websocket.send(f'PLAY:{move}')

async def join_game(game_id):
    async with websockets.connect(f'ws://localhost:5000/join/{game_id}') as websocket:
        while True:
            resp = await websocket.recv()
            print(resp)
            if resp.startswith('OPPONENT'):
                move = int(input('Column: '))
                await websocket.send(f'PLAY:{move}')

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print(f'USAGE: python {sys.argv[0]} -c OR python {sys.argv[0]} -j <game_id>')
        sys.exit(1)
    if sys.argv[1] in ('-c', '--create'):
        asyncio.run(create_game())
    elif sys.argv[1] in ('-j', '--join'):
        if len(sys.argv) != 3:
            print(f'USAGE: python {sys.argv[0]} {sys.argv[1]} <game_id>')
            sys.exit(1)
        try:
            game_id = int(sys.argv[2])
        except ValueError:
            print('Invalid game_id')
            sys.exit(1)
        asyncio.run(join_game(game_id))
