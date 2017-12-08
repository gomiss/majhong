# coding:utf-8
import rules

class DpStatus1:
    def __init__(self, pre_status, delta):
        self.pre_status = pre_status
        self.delta = delta

class OneTimeSolver:
    def __init__(self):
        self.cache = {}

    @classmethod
    def status_encode(cls, sta):
        result = 0
        first_non_zero = 0
        last_zero = rules.MAX_VALUE
        while first_non_zero < rules.MAX_VALUE and sta[first_non_zero] == 0:
            first_non_zero += 1
        while last_zero > 0 and sta[last_zero-1] == 0:
            last_zero -= 1
        for i in range(first_non_zero, last_zero):
            result = result * (rules.MAX_ITEM_COUNT + 1) + sta[i]
        return result

    def solve(self, sta):
        code = self.status_encode(sta)
        if code in self.cache:
            return self.cache[code]
        now_map = {(0, 0, 0): 0}
        dest_map = {}
        for i in range(rules.MAX_VALUE):
            dest_map = {}
            now_count = sta[i]
            for status_tuple, value in now_map.items():
                count_2 = status_tuple[0]
                count_1 = status_tuple[1]
                delta = status_tuple[2]
                for my_count in range(count_1 + count_2, min(0, now_count) + rules.MAX_ITEM_COUNT + 1):
                    new_count_1 = (my_count - count_1 - count_2) % 3
                    new_count_2 = count_1
                    new_delta = my_count - now_count + delta
                    if new_delta > rules.HAND_ITEM:
                        continue
                    new_tuple = (new_count_2, new_count_1, new_delta)
                    dest_map[new_tuple] = min(dest_map.get(new_tuple, 100), value + max(0, now_count - my_count))
            now_map, dest_map = dest_map, now_map
        result_array = []
        for i in range(-rules.HAND_ITEM, rules.HAND_ITEM + 1):
            query_tuple = (0, 0, i)
            result = now_map.get(query_tuple, 100)
            result_array.append(result)
        self.cache[code] = result_array
        return result_array


class MajhongSolver:

    def __init__(self):
        self.one_time_solver = OneTimeSolver()

    @classmethod
    def __second_dp(cls, colors_dp_result, add_count):
        total = rules.HAND_ITEM * 2 + 1
        now_st = [100] * total
        now_st[rules.HAND_ITEM] = 0
        dest_st = [0] * total
        for color_dp_result in colors_dp_result:
            dest_st = [100] * total
            for i in range(total):
                if now_st[i] > rules.HAND_ITEM:
                    continue
                for j in range(total):
                    target_index = i + j - rules.HAND_ITEM
                    if target_index < 0 or target_index >= total:
                        continue
                    dest_st[target_index] = min(dest_st[target_index], now_st[i] + color_dp_result[j])
            now_st, dest_st = dest_st, now_st
        return now_st[rules.HAND_ITEM - add_count]

    def solve(self, colors):
        colors_dp_result = []
        for i in range(rules.COLOR_COUNT):
            colors_dp_result.append(self.one_time_solver.solve(colors[i]))
        best = 100
        # 枚举将牌
        for i in range(rules.COLOR_COUNT):
            for j in range(rules.MAX_VALUE):
                tmp = [x for x in colors[i]]
                tmp[j] -= 2
                add_count = 0
                if tmp[j] < 0:
                    add_count = abs(tmp[j])
                    tmp[j] = 0
                tmp_arr = [x for x in colors_dp_result]
                tmp_arr[i] = self.one_time_solver.solve(tmp)
                second_dp_result = self.__second_dp(tmp_arr, add_count)
                best = min(second_dp_result, best)
        return best

if __name__ == '__main__':
    solver = MajhongSolver()
    solver.solve([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0, 2, 1, 0], [1, 1, 1, 0, 3, 1, 1, 0, 0]])







