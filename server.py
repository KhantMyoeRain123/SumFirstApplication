import asyncio

import websockets

import random

import json

games = {}
player_to_hex = {}

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


async def handler(websocket):
    async for message in websocket:
        event = json.loads(message)
        if event['type'] == 'join-room':
            print(event['code'])
        if event['type'] == 'make-room':
            game = Game(event['code'])
            game.players[event['playerName']] = [0, event['code']]
            games[event['code']] = game
            player_to_hex[event['playerName']] = event['code']
            print(f'A room with code '+event['code']+' has been made.')
            print(games)
            print(player_to_hex)


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
