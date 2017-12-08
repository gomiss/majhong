import random
from rules import Game
import rules
import time
import solver
import copy

def choose_drop_item(color_array, solver):
    min_sum = rules.HAND_ITEM
    min_index = -1
    can_drop = []
    for i in range(3):
        color = color_array[i]
        color_sum = sum(color)
        if color_sum < min_sum:
            min_sum = color_sum
            min_index = i
        for j in range(rules.MAX_VALUE):
            if color[j] != 3:
                for k in range(color[j]):
                    can_drop.append((i, j))
    if min_sum > 0:
        for j in range(rules.MAX_VALUE):
            if color_array[min_index][j] > 0:
                return (min_index, j)

    now_solve_count = solver.solve(color_array)
    copied = copy.deepcopy(color_array)
    besti = -1
    bestj = -1
    best_replace = 0
    for i in range(3):
        for j in range(rules.MAX_VALUE):
            if copied[i][j] > 0:
                copied[i][j] -= 1
                replace_count = 0
                for i1 in range(3):
                    for j1 in range(rules.MAX_VALUE):
                        if color_array[i1][j1] < rules.MAX_ITEM_COUNT:
                            copied[i1][j1] += 1
                            tmp_solve_count = solver.solve(copied)
                            if tmp_solve_count < now_solve_count:
                                replace_count += rules.MAX_ITEM_COUNT - color_array[i1][j1]
                            copied[i1][j1] -= 1
                if replace_count > best_replace:
                    besti = i
                    bestj = j
                    best_replace = replace_count
                copied[i][j] += 1
    if best_replace > 0:
        print(besti, bestj, best_replace)
        return (besti, bestj)
    else:
        return can_drop[random.randrange(len(can_drop))]


if __name__ == '__main__':
    game = Game()
    solver = solver.MajhongSolver()
    total = 0
    start_clock = time.clock()
    random.seed(1)
    for round in range(100):
        game.reset()
        takes = 0
        while True:
            if rules.finish_check(game.hand_item):
                print('Finish after %d takes %s' % (takes, game.get_hand_str()))
                total += 1
                break
            if not game.has_other_items():
                print('Cannot finish %s %d %d' % (game.get_hand_str(), takes, solve_result))
                break
            game.drop_and_take_item(choose_drop_item(game.hand_item, solver))

            solve_result = solver.solve(game.hand_item)
            print('%s %d' % (game.get_hand_str(), solve_result))

            takes += 1
    end_clock = time.clock()
    print(total)
    print('%.3f' % (end_clock - start_clock))




