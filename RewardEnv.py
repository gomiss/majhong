# coding:utf-8
import rules
import solver

class RewardEnv:

    def __init__(self):
        self.game = rules.Game()
        self.solver = solver.MajhongSolver()

    def __change_colors_to_vector(self, colors):
        result = []
        for color in colors:
            result += color
        return result

    def reset(self):
        self.game.reset()
        self.status = (self.solver.solve(self.game.hand_item), self.solver.count_color(self.game.hand_item))
        return self.__change_colors_to_vector(self.game.hand_item)

    @classmethod
    def __calc_reward(cls, status_before, status_after):
        score_before, color_count_before = status_before
        score_after, color_count_after = status_after
        if color_count_before != color_count_after:
            if color_count_before > color_count_after:
                return 100
            else:
                return -100
        if score_before != score_after:
            if score_before > score_after:
                return 50
            else:
                return -50
        return -1


    def step(self, action):
        action_tuple = (action // 9, action % 9)
        self.game.drop_and_take_item(action_tuple)
        observe = self.__change_colors_to_vector(self.game.hand_item)
        if rules.finish_check(self.game.hand_item):
            return observe, True, 1000
        score_after = self.solver.solve(self.game.hand_item)
        color_count_after = self.solver.count_color(self.game.hand_item)
        reward = self.__calc_reward(self.status, (score_after, color_count_after))
        finished = False
        if not self.game.has_other_items():
            finished = True
        self.status = (score_after, color_count_after)
        if finished:
            reward = self.__calc_final_reward()

        return observe, finished, reward

    def get_valid_actions(self):
        now_index = 0
        result = []
        for i in range(3):
            for j in range(9):
                if self.game.hand_item[i][j] > 0:
                    result.append(now_index)
                now_index += 1
        return result

    def get_score_tuple(self):
        return (self.solver.solve(self.game.hand_item), self.solver.count_color(self.game.hand_item))

    def get_color_number(self):
        result = []
        for i in range(3):
            result.append(sum(self.game.hand_item[i]))
        result = sorted(result)
        return '-'.join(map(lambda x:str(x), result))

    # 摸完牌还没胡
    def __calc_final_reward(self):
        result = []
        for i in range(3):
            result.append(sum(self.game.hand_item[i]))
        result = sorted(result)
        if result[0] > 1:
            return -2000  # 花猪
        return -100 * (self.status[0] + 1) # 换牌数，已下叫为0





