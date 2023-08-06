import random
import numpy as np
import sys

sys.setrecursionlimit(10000)

class position:
    """
    点击位置参数
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    def __str__(self):
        return str(self.x)+","+str(self.y)


class mine:
    def __init__(self, x: int, y: int, mine_num: int, first_check: position):
        self.x = x
        self.y = y
        self.check = first_check
        self.mine_num = mine_num
        self.mine_label = None
        self.sum_label = None
        self.label = None
        self.show_label = None
        self.position_list = []
        self.showlabel_list = []
        self.init_label()


    def init_label(self):
        self.mine_label = np.zeros((self.x, self.y), dtype=np.int)
        self.sum_label = np.zeros((self.x, self.y), dtype=np.int)
        self.label = np.zeros((self.x + 2, self.y + 2), dtype=np.int)
        self.show_label = np.zeros((self.x, self.y))
        self.show_label[np.where(self.show_label == 0)] = np.nan
        self.random_mine()
        self.flip(self.check)
        self.mine_label_s = self.write_arr(self.mine_label)
        self.sum_label_s = self.write_arr(self.sum_label)
        self.show_label_s = self.write_arr(self.show_label)
        return

    def random_mine(self):
        for i in range(self.mine_num):
            x, y = random.randint(0, self.x - 1), random.randint(0, self.y - 1)
            while x==self.check.x or y == self.check.y or self.mine_label[x,y]==1:
                x, y = random.randint(0, self.x - 1), random.randint(0, self.y - 1)
            self.mine_label[x, y] = 1
            self.label[x + 1, y + 1] = 1
        self.compute_conv()
        return

    def compute_conv(self):
        for i in range(1, self.x+1):
            for j in range(1, self.y+1):
                if self.mine_label[i - 1, j - 1] == 0:
                    self.sum_label[i - 1, j - 1] = np.sum(self.label[i - 1:i + 2, j - 1:j + 2])
        return

    def write_arr(self, arr):
        string = ""
        for i in range(self.x):
            for j in range(self.y):
                if np.isnan(arr[i, j]):
                    string += "* "
                else:
                    string += str(int(arr[i, j])) + " "
            string = string.strip(",")
            string += "\n"
        return string

    def flip(self, pos: position):
        if self.mine_label[pos.x, pos.y] == 1:
            return True
        if self.sum_label[pos.x, pos.y] == 0:
            # 深度搜索
            self.dfs(pos.x, pos.y)
        else:
            self.show_label[pos.x, pos.y] = self.sum_label[pos.x, pos.y]
        self.showlabel_list.append(np.copy(self.show_label))
        self.position_list.append(pos)
        return False

    def dfs(self, x, y):
        if x >= self.x or x < 0 or y >= self.y or y < 0 or \
                self.mine_label[x, y] == 1 or not np.isnan(self.show_label[x, y]):
            return
        elif self.sum_label[x,y]!=0:
            self.show_label[x, y] = self.sum_label[x, y]
            return
        else:
            self.show_label[x, y] = self.sum_label[x, y]
            self.dfs(x - 1, y)
            self.dfs(x + 1, y)
            self.dfs(x, y + 1)
            self.dfs(x, y - 1)
        return

    def checkwin(self):
        index = np.where(self.show_label==-1)
        if len(index[0])==self.mine_num:
            for i,j in zip(index[0],index[1]):
                if self.show_label[i,j]==-1:
                    continue
                else:
                    print("cuowu",i,",",j)
                    return True,False
            return True,True
        else:
            for i,j in zip(index[0],index[1]):
                if self.mine_label[i,j]!=1:
                    print("wrong mine ",i,":",j)
                    return True,False
            return False,None



if __name__ == '__main__':
    M = mine(9, 9, 10, position(5, 6))
    print(M.show_label_s)
    print(M.sum_label_s)
    print(M.mine_label_s)