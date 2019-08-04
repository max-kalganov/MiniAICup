import json
from typing import Union, Dict

from my_strategy.constants import TYPE, TYPE_END_GAME, TYPE_START_GAME
from my_strategy.main_strategy import MainStrategy


def get_res(cur_state: Dict) -> Union[None, str]:
    if cur_state[TYPE] in {TYPE_END_GAME, TYPE_START_GAME}:
        ms.setup_stats(cur_state)
        return None
    else:
        cmd = ms.get_command(cur_state)
        return cmd


ms = MainStrategy()
while True:
    state = input()
    cmd = ms.get_command(json.loads(state))
    if cmd:
        print(json.dumps({"command": cmd, 'debug': str(state)}))