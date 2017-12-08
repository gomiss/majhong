import random
import logging

MAX_VALUE = 9
HAND_ITEM = 14
COLOR_COUNT = 3
MAX_ITEM_COUNT = 4

class Game():
    def __init__(self):
        self.left_item = []
        self.hand_item = [[], [], []]

    def reset(self):
        tmp_list = []
        for i in range(3):
            for j in range(MAX_VALUE):
                for k in range(4):
                    tmp_list.append((i, j))
        random.shuffle(tmp_list)
        self.left_item = []
        for i in range(0, len(tmp_list), 4):
            self.left_item.append(tmp_list[i])
        self.hand_item = [[0] * MAX_VALUE, [0] * MAX_VALUE, [0] * MAX_VALUE]
        for i in range(HAND_ITEM):
            next_item = self.get_next_item()
            self.hand_item[next_item[0]][next_item[1]] += 1

    def get_next_item(self):
        result = self.left_item[-1]
        self.left_item.pop()
        return result

    def has_other_items(self):
        return len(self.left_item) > 0

    def drop_and_take_item(self, drop_item_tuple):
        if self.hand_item[drop_item_tuple[0]][drop_item_tuple[1]] == 0:
            logging.error('drop (%d %d) which not in hand' % drop_item_tuple)
        else:
            self.hand_item[drop_item_tuple[0]][drop_item_tuple[1]] -= 1
            next_item = self.get_next_item()
            self.hand_item[next_item[0]][next_item[1]] += 1

    def get_hand_str(self):
        symbol = 'abc'
        result_list = []
        for i in range(3):
            color = self.hand_item[i]
            for j in range(MAX_VALUE):
                for k in range(color[j]):
                    result_list.append('%s%d' % (symbol[i], j))
        return ','.join(result_list)

def single_color_finish_check(color):
    copy_array = [x for x in color]
    for i in range(MAX_VALUE):
        if copy_array[i] >= 3:
            copy_array[i] -= 3
        if copy_array[i] > 0:
            if i + 2 >= MAX_VALUE:
                return False
            for j in range(i + 1, i + 3):
                if copy_array[j] < copy_array[i]:
                    return False
                copy_array[j] -= copy_array[i]
    return True


def finish_check(color_array):
    color_count = 0
    for color in color_array:
        if sum(color) > 0:
            color_count += 1
    if color_count > 2:
        return False
    for color in color_array:
        other_finish = True
        if sum(color) == 0:
            continue
        for color2 in color_array:
            if color2 is not color and not single_color_finish_check(color2):
                other_finish = False
                break
        if not other_finish:
            continue
        for i in range(9):
            if color[i] >= 2:
                color[i] -= 2
                if single_color_finish_check(color):
                    color[i] += 2
                    return True
                color[i] += 2



