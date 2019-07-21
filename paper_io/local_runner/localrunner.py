from asyncio import events
import argparse

import pyglet
from pyglet.window import key

from local_runner.helpers import TERRITORY_CACHE
from local_runner.clients import KeyboardClient, SimplePythonClient, FileClient, StrategyClient
from local_runner.constants import LR_CLIENTS_MAX_COUNT, MAX_TICK_COUNT
from local_runner.game_objects.scene import Scene
from local_runner.game_objects.game import LocalGame

scene = Scene()
loop = events.new_event_loop()
events.set_event_loop(loop)

parser = argparse.ArgumentParser(description='LocalRunner for paperio')

for i in range(1, LR_CLIENTS_MAX_COUNT + 1):
    parser.add_argument('-p{}'.format(i), '--player{}'.format(i), type=str, nargs='?',
                        help='Path to executable with strategy for player {}'.format(i))
    parser.add_argument('--p{}l'.format(i), type=str, nargs='?', help='Path to log for player {}'.format(i))

parser.add_argument('-t', '--timeout', type=str, nargs='?', help='off/on timeout', default='on')

args = parser.parse_args()

clients = []
for i in range(1, LR_CLIENTS_MAX_COUNT + 1):
    arg = getattr(args, 'player{}'.format(i))
    if arg:
        if arg == 'keyboard':
            client = KeyboardClient(scene.window)
        elif arg == 'simple_bot':
            client = SimplePythonClient()
        elif arg == 'strategy':
            client = StrategyClient()
        else:
            client = FileClient(arg.split(), getattr(args, 'p{}l'.format(i)))

        clients.append(client)

if len(clients) == 0:
    clients.append(KeyboardClient(scene.window))


class Runner:
    @staticmethod
    def game_loop_wrapper(dt):
        is_game_over = loop.run_until_complete(Runner.game.game_loop())
        if is_game_over or (args.timeout == 'on' and Runner.game.tick >= MAX_TICK_COUNT):
            loop.run_until_complete(Runner.game.game_loop())
            Runner.game.send_game_end()
            Runner.game.game_save()
            Runner.stop_game()

    @staticmethod
    @scene.window.event
    def on_key_release(symbol, modifiers):
        if symbol == key.R:
            Runner.stop_game()
            TERRITORY_CACHE.clear()
            Runner.run_game()

    @staticmethod
    def stop_game():
        pyglet.clock.unschedule(Runner.game_loop_wrapper)

    @staticmethod
    def run_game():
        # draw_window = True, schedule_interval(Runner.game_loop_wrapper, 0.01) - for visualizing
        # draw_window = False, schedule_interval(Runner.game_loop_wrapper, 0.0000000001) - for not visualizing

        Runner.game = LocalGame(clients, scene, args.timeout == 'on', draw_window=True)
        Runner.game.send_game_start()
        pyglet.clock.schedule_interval(Runner.game_loop_wrapper, 0.01)


Runner.run_game()
pyglet.app.run()
