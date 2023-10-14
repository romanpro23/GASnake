from genetic_algoritm.brainV1 import *
from brain_net.brain_netV1 import *
from genetic_algoritm.snake import Snake
import numpy as np
import random


class SnakeAI(Snake):
    def __init__(self, length, height, width, count_layer=1, hidden=64):
        super().__init__(length, height, width)
        self.brain = Brain(model=BrainNetV1(11, hidden, 3, count_layer=count_layer))
        self.count_layer = count_layer
        self.hidden = hidden
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.color_head = (r, g, b)

    def new(self):
        super().new()

    def review(self, board, food):
        x0, y0 = self.body[0]
        check_wall = x0 >= self.width or y0 >= self.height
        point_r = True if (x0 + 1 >= self.width or check_wall) else (board[x0 + 1][y0] == -1.0)
        point_l = True if (x0 - 1 < 0 or check_wall) else (board[x0 - 1][y0] == -1.0)
        point_d = True if (y0 + 1 >= self.height or check_wall) else (board[x0][y0 + 1] == -1.0)
        point_u = True if (y0 - 1 < 0 or check_wall) else (board[x0][y0 - 1] == -1.0)

        dir_l = self.dx == -1
        dir_r = self.dx == 1
        dir_u = self.dy == -1
        dir_d = self.dy == 1

        result = np.array(
            [
                # Danger Straight
                (dir_u and point_u) or
                (dir_d and point_d) or
                (dir_l and point_l) or
                (dir_r and point_r),

                # Danger right
                (dir_u and point_r) or
                (dir_d and point_l) or
                (dir_u and point_u) or
                (dir_d and point_d),

                # Danger Left
                (dir_u and point_r) or
                (dir_d and point_l) or
                (dir_r and point_u) or
                (dir_l and point_d),

                self.dx == 1,
                self.dx == -1,
                self.dy == 1,
                self.dy == -1,
                x0 < food.x,
                x0 > food.x,
                y0 < food.y,
                y0 > food.y
            ], np.float32)
        return result

    def action(self, board, food):
        state = self.review(board, food)

        return self.brain.action(state)