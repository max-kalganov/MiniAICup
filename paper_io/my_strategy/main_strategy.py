from typing import Union, List
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

            cells_territory = self.get_cell(np.array(player_state[TERRITORY]))
            self.set_markers(coords=cells_territory,
                             marker=marker)

            cells_lines = self.get_cell(np.array(player_state[LINES]))
            self.set_markers(coords=cells_lines,
                             marker=marker + LINES_MARKER_ADDITION)

            head_pos = self.get_cell(np.array(player_state[POSITION]))
            self.set_markers(coords=head_pos,
                             marker=marker + HEAD_MARKER_ADDITION)

        cells_bonuses = self.get_cell(np.array([bonus[POSITION] for bonus in state_params[BONUSES]]))
        self.set_markers(coords=cells_bonuses,
                         marker=BONUS_MARKER)

    def init_map(self, settings):
        self.map = np.zeros([settings[PARAMS][X_CELLS_COUNT],
                             settings[PARAMS][Y_CELLS_COUNT]])

    def set_markers(self,
                    coords: np.ndarray,
                    marker: float) -> bool:
        assert isinstance(coords, np.ndarray), f"wrong type of coords"

        if coords.size == 0:
            return False

        if coords.size == 2:
            self.map[coords[0], coords[1]] = marker
        else:
            self.map[coords[:, 0], coords[:, 1]] = marker
        return True

    def get_cell(self, coord_with_width):
        return (coord_with_width - 15) // 30

    def calc_step(self) -> Union[UP, LEFT, RIGHT, DOWN]:
        return UP

    # Bug: method doesn't print info
    def get_command(self, state: dict) -> Union[UP, DOWN, LEFT, RIGHT]:
        # self.ticks = pd.concat([self.ticks, pd.DataFrame(state['params'])])
        self.update_map(state[PARAMS])
        print(f"tick = {state['params']['tick_num']}\n ")
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                print(int(10*self.map[i, j]), end=" ")
            print("")
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
