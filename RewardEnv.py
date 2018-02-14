# coding:utf-8
import rules
import solver


class RewardEnv:

    def __init__(self):
        self.game = rules.Game()
        self.solver = solver.MajhongSolver()

    def __change_colors_to_vector(self, colors):
        result = []
        for i in range(len(colors)):
            if i == self.dropped_color:
                continue
            color = colors[i]
            for cnt in color:
                for j in range(rules.MAX_ITEM_COUNT+1):
                    result.append(1 if j == cnt else 0)
        return result

    def reset(self):
        self.game.reset()
        self.status = (self.solver.solve(self.game.hand_item), self.solver.count_color(self.game.hand_item))
        self.dropped_color = 0
        for i in range(1, 3):
            if sum(self.game.hand_item[i]) < sum(self.game.hand_item[self.dropped_color]):
                self.dropped_color = i
        return self.step(None)

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

    def clean_hand(self): # 无脑打直到缺或结束
        while sum(self.game.hand_item[self.dropped_color]) > 0 and self.game.has_other_items():
            for i in range(0, rules.MAX_VALUE):
                if self.game.hand_item[self.dropped_color][i] > 0:
                    self.game.drop_and_take_item((self.dropped_color, i))
                    break


    def step(self, action):
        if action is not None:
            color = action // 9
            if color >= self.dropped_color:
                color += 1
            action_tuple = (color, action % 9)
            if self.game.hand_item[action_tuple[0]][action_tuple[1]] <= 0:
                return self.__change_colors_to_vector(self.game.hand_item), False, -200
            self.game.drop_and_take_item(action_tuple)
        self.clean_hand()
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





