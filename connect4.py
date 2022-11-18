import argparse
import asyncio
import websockets

async def create_game(server_ip='localhost'):
    async with websockets.connect(f'ws://{server_ip}:5000/create') as websocket:
        while True:
            resp = await websocket.recv()
            print(resp)
            if resp == 'GAMESTART' or resp.startswith('OPPONENT'):
                move = int(input('Column: '))
                await websocket.send(f'PLAY:{move}')

async def join_game(game_id, server_ip='localhost'):
    async with websockets.connect(f'ws://{server_ip}:5000/join/{game_id}') as websocket:
        while True:
            resp = await websocket.recv()
            print(resp)
            if resp.startswith('OPPONENT'):
                move = int(input('Column: '))
                await websocket.send(f'PLAY:{move}')

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
        print(args.join)
        asyncio.run(join_game(args.join))
    else:
        parser.print_help()
