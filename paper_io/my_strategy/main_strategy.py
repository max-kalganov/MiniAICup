class MainStrategy:
    def __init__(self):
        self.steps = ['up', 'right', 'down', 'left']
        self.cur_index = 0
        self.cur_step = -1
        self.num_of_steps = 0
        self.circle_start = self.steps[self.cur_index - 1]
        self.circle_num = 0

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

    # TODO: add border check to the strategy
    # TODO: check start direction. If it is down - change cur_index in init
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

    def get_command(self, state):
        self.calc_new_step()
        return self.steps[self.cur_index]
