from typing import Union
import pandas as pd
import numpy as np

from my_strategy.constants import UP, RIGHT, LEFT, DOWN, TYPE, TYPE_START_GAME, PARAMS, X_CELLS_COUNT, Y_CELLS_COUNT, \
    SPEED, PLAYERS, TERRITORY, LINES, POSITION, LINES_MARKER_ADDITION, HEAD_MARKER_ADDITION, BONUSES, BONUS_MARKER, \
    CELL_WIDTH


class MainStrategy:
    def __init__(self):
        self.map = None
        self.speed = None
        self.width = None

    def setup_stats(self, settings: dict):
        if settings[TYPE] == TYPE_START_GAME:
            self.init_map(settings)
            self.speed = settings[PARAMS][SPEED]
            self.width = settings[PARAMS][CELL_WIDTH]

    def update_map(self, state_params):
        for player_index, player_state in state_params[PLAYERS].items():
            if player_index == 'i':
                marker = -1
            else:
                marker = int(player_index)

            cells_territory = (np.array(player_state[TERRITORY]) - 15)//30
            self.map[cells_territory[:, 0], cells_territory[:, 1]] = marker

            cells_lines = (np.array(player_state[LINES])-15)//30
            self.map[cells_lines[:, 0], cells_lines[:, 1]] = marker + LINES_MARKER_ADDITION

            self.map[(player_state[POSITION][0]-15)//30,
                     (player_state[POSITION][0]-15)//30] = marker + HEAD_MARKER_ADDITION

        cells_bonuses = (np.array([bonus[POSITION] for bonus in state_params[BONUSES]]))-15//30
        self.map[cells_bonuses[:, 0], cells_bonuses[:, 1]] = BONUS_MARKER

    def init_map(self, settings):
        self.map = np.zeros([settings[PARAMS][X_CELLS_COUNT],
                             settings[PARAMS][Y_CELLS_COUNT]])

    def calc_step(self) -> Union[UP, LEFT, RIGHT, DOWN]:
        return UP

    # Bug: method doesn't print info
    def get_command(self, state: dict) -> Union[UP, DOWN, LEFT, RIGHT]:
        # self.ticks = pd.concat([self.ticks, pd.DataFrame(state['params'])])
        self.update_map(state[PARAMS])
        print('tick = ', state['params']['tick_num'], '\n', self.map)
        return self.calc_step()


class SimpleBot:
    def __init__(self):
        self.steps = [UP, RIGHT, DOWN, LEFT]
        self.cur_index = 0
        self.cur_step = -1
        self.num_of_steps = 0
        self.circle_start = self.steps[self.cur_index - 1]
        self.circle_num = 0

        self.first_stats = None
        self.ticks = pd.DataFrame()
        self.map = None
        self.speed = None
        self.width = None

    def setup_stats(self, settings: dict):
        self.first_stats = pd.DataFrame(settings)
        if settings[TYPE] == TYPE_START_GAME:
            self.init_map(settings)
            self.speed = settings[PARAMS][SPEED]
            self.width = settings[PARAMS][CELL_WIDTH]

    def get_next_index(self):
        new_cur_index = self.cur_index + 1
        if len(self.steps) <= new_cur_index:
            new_cur_index = 0
        return new_cur_index

    def get_prev_index(self):
        new_cur_index = self.cur_index - 1
        if new_cur_index < 0:
            new_cur_index = len(self.steps) - 1
        return new_cur_index

    def calc_new_step(self):
        if self.cur_step == self.num_of_steps:
            self.cur_step = 0
            if self.steps[self.cur_index] == self.circle_start:
                self.circle_start = self.steps[self.get_prev_index()]
                self.circle_num += 1
                if self.circle_num == 4:
                    self.num_of_steps += 1
                    self.circle_num = 0
            else:
                self.cur_index = self.get_next_index()
        else:
            self.cur_step += 1

    def update_map(self, state):
        pass

    def init_map(self, settings):
        self.map = np.zeros([settings[PARAMS][X_CELLS_COUNT],
                             settings[PARAMS][Y_CELLS_COUNT]])

    def get_command(self, state: dict) -> Union[UP, DOWN, LEFT, RIGHT]:
        # self.ticks = pd.concat([self.ticks, pd.DataFrame(state['params'])])

        self.calc_new_step()
        return self.steps[self.cur_index]
