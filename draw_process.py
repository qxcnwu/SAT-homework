import sys
import time
import pygame
import os
import numpy as np

from save_log import load_log


def load_image(SIZE):
    dir = "resource/"
    dic = {}
    for i in range(-2, 9):
        path = os.path.join(dir, str(i) + ".png")
        img = pygame.image.load(path).convert()
        img = pygame.transform.smoothscale(img, (SIZE, SIZE))
        dic.update({
            i: img
        })
    return dic


def main(position_list, process_list, SIZE=20):
    kmax = process_list.shape[2]
    k = 0

    pygame.init()
    screen = pygame.display.set_mode((1400, 800))
    pygame.display.set_caption('结果绘制')
    screen.fill((242, 242, 242))
    pygame.display.flip()
    running = True
    pic_dic = load_image(SIZE)

    # 绘制初始化地图
    x, y = process_list[:,:,0].shape
    for i in range(x):
        for j in range(y):
            pos = (SIZE+j * SIZE, SIZE+i * SIZE)
            screen.blit(pic_dic[-2], pos)
    pygame.display.update()
    time.sleep(0.5)

    while k < kmax and running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        temp_screen = process_list[:,:,k]
        temp_screen[np.where(np.isnan(temp_screen))] = -2
        x, y = temp_screen.shape
        for i in range(x):
            for j in range(y):
                pos = (SIZE+j * SIZE, SIZE+i * SIZE)
                screen.blit(pic_dic[temp_screen[i, j]], pos)
        k += 1
        time.sleep(0.1)
        pygame.display.update()
    time.sleep(500)
    sys.exit()


if __name__ == '__main__':
    a, b = load_log("answer/save3.npy")
    main(b, a,20)
