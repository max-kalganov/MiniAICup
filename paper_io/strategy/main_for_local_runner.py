import json
from time import sleep

from strategy.strategy import get_command

STATE: bytes = None


def _set_state(msg: bytes):
    global STATE
    STATE = msg


def get_state() -> str:
    global STATE
    while not STATE: sleep(0.001)
    state = STATE.decode('utf-8')
    STATE = None
    return state


def run_main():
    while True:
        state = get_state()
        cmd = get_command(state)
        yield json.dumps({"command": cmd, 'debug': str(state)})


if __name__ == '__main__':
    _set_state("some state".encode('utf-8'))
    print(run_main())
    _set_state("some state".encode('utf-8'))
    print(run_main())
    _set_state("some state".encode('utf-8'))
    print(run_main())
