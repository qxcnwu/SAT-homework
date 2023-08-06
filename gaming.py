import time
import numpy as np

from save_log import save_log,load_log
from mine_clearance import mine, position
from slover_mine import Solver_mine
from draw_process import main

def found_position(show_array):
    x, y = show_array.shape
    temp_choice = np.zeros(show_array.shape)

    def quezz(solver_array):
        if np.isnan(np.max(solver_array)) and not np.isnan(solver_array[1, 1]) and solver_array[1,1]!=-1:
            sm = Solver_mine(solver_array)
            sm.solve_Main()
            return sm.parse_answer()
        else:
            return np.zeros((3,3))

    # 轮询求解 如果判断确定是雷则标记为-1 如果确定不为雷则标记为1
    # 如果存在多个答案则确定更具相关单位确定最大的值
    # 如果只有单一值则直接确定
    # 对于值位于0~1之间

    # 求解中心点不在边缘的3x3方格的权重
    for i in range(1, x - 1):
        for j in range(1, y - 1):
            solver_array = np.copy(show_array[i - 1:i + 2, j - 1:j + 2])
            temp_choice[i - 1:i + 2, j - 1:j + 2] += quezz(solver_array)

    # 对于中心点位于边缘而不在四个脚点上的权重
    # 对于边缘采用补齐的方式求解
    for i in range(1, x - 1):
        # 左列
        solver_array = np.zeros((3, 3))
        solver_array[:, 1:] = np.copy(show_array[i - 1:i + 2, 0:2])
        temp_choice[i - 1:i + 2, 0:2] += quezz(solver_array)[:, 1:]
        # 右列
        solver_array = np.zeros((3, 3))
        solver_array[:, 0:2] = np.copy(show_array[i - 1:i + 2, y - 2:y])
        temp_choice[i - 1:i + 2, y - 2:y] += quezz(solver_array)[:, 0:2]
    for i in range(1, y - 1):
        # 上行
        solver_array = np.zeros((3, 3))
        solver_array[1:, :] = np.copy(show_array[0:2, i - 1:i + 2])
        temp_choice[0:2, i - 1:i + 2] += quezz(solver_array)[1:, :]
        # 下行
        solver_array = np.zeros((3, 3))
        solver_array[0:2, :] = np.copy(show_array[x - 2:x, i - 1:i + 2])
        temp_choice[x - 2:x, i - 1:i + 2] += quezz(solver_array)[0:2, :]

    # 填充角点
    # 左上角
    solver_array = np.zeros((3, 3))
    solver_array[1:3, 1:3] = np.copy(show_array[0:2, 0:2])
    temp_choice[0:2, 0:2] += quezz(solver_array)[1:3, 1:3]
    # 左下角
    solver_array = np.zeros((3, 3))
    solver_array[0:2, 1:3] = np.copy(show_array[x-2:x, 0:2])
    temp_choice[x-2:x, 0:2] += quezz(solver_array)[0:2, 1:3]
    # 右上角
    solver_array = np.zeros((3, 3))
    solver_array[1:3,0:2] = np.copy(show_array[0:2,y-2:y])
    temp_choice[0:2,y-2:y] += quezz(solver_array)[1:3, 0:2]
    # 右下角
    solver_array = np.zeros((3, 3))
    solver_array[0:2,0:2] = np.copy(show_array[x-2:x,y-2:y])
    temp_choice[x-2:x,y-2:y] += quezz(solver_array)[0:2,0:2]

    return temp_choice


def find_mine(temp_choice,show_array):
    """
    如果有确定为雷的地方需要重新计算相关可信系数
    :param temp_choice:
    :param show_array:
    :return:
    """
    index=np.where(temp_choice>2)
    while len(index[0])!=0:
        show_array[index[0],index[1]]=-1
        temp_choice=found_position(show_array)
        index = np.where(temp_choice > 2)
    return temp_choice


def click_choice(temp_choice: np.array) -> position:
    """
    根据计算得到的权重函数选择下一步点击的点
    :param temp_choice:
    :return:
    """
    if np.min(temp_choice) < 0:
        index = np.where(temp_choice == np.min(temp_choice))
    else:
        temp_choice[temp_choice == 0] = 999
        index = np.where(temp_choice == np.min(temp_choice))
    return position(index[0][0], index[1][0])


def Process_Main(M: mine):
    finish = False
    win = False
    while not finish:
        temp_choice = found_position(M.show_label)
        find_mine(temp_choice,M.show_label)
        position = click_choice(temp_choice)
        finish=M.flip(position)
        print(position)
        print(M.write_arr(M.show_label))
        if finish:
            print("错误的雷")
            break
        finish, win = M.checkwin()
    if win:
        print("win")
    else:
        print("boom")
    return


if __name__ == '__main__':
    start=time.time()
    M = mine(16, 16, 20, position(5, 6))
    Process_Main(M)
    print(time.time()-start)
    save_log(M,"answer/save3")
    a, b = load_log("answer/save3.npy")
    main(b, a,30)
