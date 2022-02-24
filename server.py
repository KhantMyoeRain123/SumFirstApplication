import asyncio
from distutils.log import error

import websockets

import random

import json

games = {}
player_to_hexws = {}

# copied from discord bot project not final and will have to adjust


class Game:
    def __init__(self, code):
        self.code = code
        self.players = {}
        self.sequence = []
        self.emp_str = ''
        self.answered = {}
        self.question_asked = False
        self.resolving = False
        self.ws = []
        self.started = False

    def generate_question(self):
        num_of_num = random.randint(3, 10)
        for i in range(num_of_num):
            num = random.randint(1, 9)
            self.sequence.append(num)

        return f'Find the sum to this sequence:{self.emp_str.join(str(self.sequence))}'

    async def resolve_answers(self):
        if(len(self.answered) != len(self.players)):
            return
        if(self.resolving):
            return
        count = 0
        self.resolving = True
        for playerinfo in self.players.values():
            await playerinfo[0].send(f'The answer is:{sum(self.sequence)}')
        for player_name, answer in self.answered.items():
            if answer == sum(self.sequence):
                self.players[player_name][1] += len(self.sequence)-count
                for playerinfo in self.players.values():
                    await playerinfo[0].send(f'{player_name} got {len(self.sequence)-count} points!! {player_name} has {self.players[player_name][1]} points now!!')
                count += 1
        self.sequence.clear()
        self.answered.clear()
        self.question_asked = False

# handle room joining and making


async def handler(websocket):
    async for message in websocket:
        event = json.loads(message)
        if event['type'] == 'join-room':
            if(event['code'] in games):
                games[event['code']].players[event['playerName']] = [
                    0, event['code']]
                player_to_hexws[event['playerName']] = [
                    event['code'], websocket]
                games[event['code']].ws.append(websocket)
                # DEBUG PRINTS
                print(f'Player has joined room with code{event["code"]}')
                print(games)
                print(player_to_hexws)
                print(games[event['code']].ws)
                await play(websocket, event['code'])
            else:
                print('ERROR')
                reply = {'type': 'error', 'msg': 'Room does not exist.'}
                await websocket.send(json.dumps(reply))

        if event['type'] == 'make-room':
            game = Game(event['code'])
            game.players[event['playerName']] = [0, event['code']]
            game.ws.append(websocket)
            games[event['code']] = game
            player_to_hexws[event['playerName']] = [event['code'], websocket]
            # DEBUG PRINTS
            print(f'A room with code {event["code"]} has been made.')
            print(games)
            print(player_to_hexws)
            print(game.ws)

            await start(websocket, event['code'])


# start the game after entering the room
async def start(websocket, code):
    message = await websocket.recv()
    event = json.loads(message)
    if event['type'] == 'start':
        games[code].started = True
        await play(websocket, code)


# game loop
async def play(websocket, code):
    while True:
        if(games[code].started):
            pass


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever}


if __name__ == "__main__":
    asyncio.run(main())
