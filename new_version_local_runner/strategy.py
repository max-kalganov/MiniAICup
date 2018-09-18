import datetime
import gzip
import json

import os
import random

import pyglet
import asyncio
from subprocess import Popen, PIPE

from mechanic.constants import MAX_EXECUTION_TIME, REQUEST_MAX_TIME


class Client(object):
    @asyncio.coroutine
    def get_command(self):
        pass

    def close(self):
        pass

    @asyncio.coroutine
    def send_message(self, t, d):
        pass

    def save_log_to_disk(self, log, path):
        pass

    def get_solution_id(self):
        return random.randint(11000, 12000)


class KeyboardClient(Client):
    @property
    def KEY_COMMAND_MAP(self):
        return {
            pyglet.window.key.A: 'left',
            pyglet.window.key.D: 'right',
            pyglet.window.key.S: 'stop',
        }

    def __init__(self, window):
        self.last_pressed_button = pyglet.window.key.S

        @window.event
        def on_key_press(symbol, _):
            self.last_pressed_button = symbol

        @window.event
        def on_key_release(symbol, _):
            if symbol in [pyglet.window.key.A, pyglet.window.key.D]:
                self.last_pressed_button = pyglet.window.key.S

    @asyncio.coroutine
    def get_command(self):
        with open("/home/mr_neither/Work/PycharmProjects/MiniAICup/KeyboardDebug", "a") as f:
            t = self.KEY_COMMAND_MAP.get(self.last_pressed_button, 'stop')
            if t == 'left':
                f.write('0 ')
            elif t == 'right':
                f.write('1 ')
            elif t == 'stop':
                f.write('2 ')
            else:
                f.write('3 ')

        return {'command': self.KEY_COMMAND_MAP.get(self.last_pressed_button, 'stop')}

    def save_log_to_disk(self, log, path):
        with open("logGame", 'w') as f:
            f.write(json.dumps(log))
        return {
            'filename': os.path.basename("logGame"),
            'is_private': True,
            'location': "logGame"
        }


class FileClient(Client):
    def __init__(self, path_to_script, path_to_log=None):
        self.process = Popen(path_to_script, stdout=PIPE, stdin=PIPE)
        self.last_message = None
        if path_to_log is None:
            self.path_to_log = "/home/mr_neither/Work/PycharmProjects/MiniAICup/1.log"
        else:
            self.path_to_log = "/home/mr_neither/Work/PycharmProjects/MiniAICup/1.log"

    @asyncio.coroutine
    def send_message(self, t, d):
        msg = {
            'type': t,
            'params': d
        }
        msg_bytes = '{}\n'.format(json.dumps(msg)).encode()

        self.process.stdin.write(msg_bytes)
        self.process.stdin.flush()

    @asyncio.coroutine
    def get_command(self):
        try:
            line = self.process.stdout.readline().decode('utf-8')
            state = json.loads(line)
            return state
        except Exception as e:
            return {'debug': str(e)}

    def save_log_to_disk(self, log, _):
        with open(self.path_to_log, 'w') as f:
            f.write(json.dumps(log))

        return {
            'filename': os.path.basename(self.path_to_log),
            'is_private': True,
            'location': self.path_to_log
        }


class TcpClient(Client):
    EXECUTION_LIMIT = datetime.timedelta(seconds=MAX_EXECUTION_TIME)

    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.execution_time = datetime.timedelta()
        self.solution_id = None

    def save_log_to_disk(self, log, path):
        location = path.format(str(self.solution_id+1))

        with open(location, 'wb') as f:
            f.write(json.dumps(log))

        return {
            'filename': os.path.basename(location),
            'is_private': True,
            'location': location
        }

    @asyncio.coroutine
    def set_solution_id(self):
        hello_json = yield from asyncio.wait_for(self.reader.readline(), timeout=REQUEST_MAX_TIME)
        try:
            self.solution_id = json.loads(hello_json.decode('utf-8')).get('solution_id')
        except ValueError:
            pass

        return bool(self.solution_id)

    @asyncio.coroutine
    def send_message(self, t, d):
        msg = {
            'type': t,
            'params': d
        }
        msg_bytes = '{}\n'.format(json.dumps(msg)).encode()
        self.writer.write(msg_bytes)
        yield from self.writer.drain()

    @asyncio.coroutine
    def get_command(self):
        try:
            before = datetime.datetime.now()
            z = yield from asyncio.wait_for(self.reader.readline(), timeout=REQUEST_MAX_TIME)
            if not z:
                raise ConnectionError('Connection closed')
            self.execution_time += (datetime.datetime.now() - before)
            if self.execution_time > self.EXECUTION_LIMIT:
                raise Exception('sum timeout error')
        except asyncio.TimeoutError:
            raise asyncio.TimeoutError('read timeout error')
        try:
            z = json.loads(z.decode())
        except ValueError:
            z = {'debug': 'cant pars json'}

        return z

    def close(self):
        self.writer.close()

    def get_solution_id(self):
        return self.solution_id
