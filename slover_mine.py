import numpy as np
from z3 import *


class Solver_mine:
    def __init__(self, data_array):
        self.data_array = data_array
        self.x00, self.x01, self.x02, self.x10, self.x11, self.x12, self.x20, self.x21, self.x22 = Ints(
            'x00 x01 x02 x10 x11 x12 x20 x21 x22')
        self.parse_dict = {
            "00": self.x00,
            "01": self.x01,
            "02": self.x02,
            "10": self.x10,
            "11": self.x11,
            "12": self.x12,
            "20": self.x20,
            "21": self.x21,
            "22": self.x22
        }
        self.index_list = ["0", "1", "2"]
        self.s = Solver()
        self.init_solver()
        self.answer_m = []
        self.solution = np.copy(self.data_array)

    def init_solver(self):
        for idx, i in enumerate(self.index_list):
            for jdx, j in enumerate(self.index_list):
                if np.isnan(self.data_array[idx][jdx]):
                    self.s.add(self.parse_dict.get(i + j) >= 0)
                    self.s.add(self.parse_dict.get(i + j) <= 1)
                elif self.data_array[idx][jdx] == -1:
                    self.s.add(self.parse_dict.get(i + j) == 1)
                else:
                    self.s.add(self.parse_dict.get(i + j) == 0)
        self.sum = self.x00 + self.x01 + self.x02 + self.x10 + self.x11 + self.x12 + self.x20 + self.x21 + self.x22
        self.s.add(self.sum == self.data_array[1, 1])
        return

    def solve_Main(self):
        while (self.s.check() == sat):
            condition = []
            m = self.s.model()
            p = ""
            for i in self.index_list:
                for j in self.index_list:
                    temp = self.parse_dict.get(i + j)
                    p += chr(int("%s" % (m[temp])))
                    condition.append(temp != int("%s" % (m[temp])))
            self.s.add(Or(condition))
            self.answer_m.append(m)
        return

    def parse_answer(self):
        # 判断有几个answer 如果只有一个则可以直接赋值
        # 如果拥有多个则以0.1的系数增加
        k = 1 if len(self.answer_m) == 1 else 0.1
        for idx, i in enumerate(self.index_list):
            for jdx, j in enumerate(self.index_list):
                if np.isnan(self.solution[idx, jdx]):
                    self.solution[idx, jdx] = sum([int(str(m[self.parse_dict.get(i + j)])) for m in self.answer_m]) * k
                else:
                    self.solution[idx, jdx] = 0
        if (k == 1):
            # 一定不是雷标记-5
            self.solution[np.logical_and(self.solution == 0, np.isnan(self.data_array))] = -5
            # 一定是雷标记2
            self.solution[self.solution==1]=2
        return self.solution


if __name__ == '__main__':
    data = np.array([[np.nan, 1, 1], [1, 0, 1], [1, 1, 1]])
    sm = Solver_mine(data)
    sm.solve_Main()
    so = sm.parse_answer()
