import pygame
import numpy as np

black = (0, 0, 0)
white = (255, 255, 255)

count_h = 3
count_w = 4
h = 30
w = 40
height = h * count_h + (count_h + 1)
width = w * count_w + (count_w + 1)
size_block = 8
snake_block = 7
pad = 33

border = size_block

dis_width = width * size_block
dis_height = height * size_block + pad

pygame.init()
clock = pygame.time.Clock()
display = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake arena')
snake_speed = 1000


def make_board(snake, foods, others):
    board = np.zeros((w, h), np.float32)
    for x, y in snake.body:
        if 0 <= x < w and 0 <= y < h:
            board[x][y] = -1.0

    for food in foods:
        board[food.x][food.y] = 1.0

    return board


def draw_borders(score, epsilon, max_score, generation=None):
    pygame.draw.rect(display, white, [0, pad, dis_width, border])
    pygame.draw.rect(display, white, [0, 0, dis_width, border])
    pygame.draw.rect(display, white, [0, dis_height - border, dis_width, border])
    pygame.draw.rect(display, white, [dis_width - border, 0, border, dis_height])
    pygame.draw.rect(display, white, [0, 0, border, dis_height])
    start_position = []
    for i in range(count_w):
        pygame.draw.rect(display, white, [i * border + i * w * size_block, pad, border, dis_height - pad])
    for i in range(count_h):
        pygame.draw.rect(display, white, [0, i * border + i * h * size_block + pad, dis_width, border])

    for i in range(count_w):
        for j in range(count_h):
            start_position.append((i * border + i * w * size_block, j * border + j * h * size_block + pad))

    score_font = pygame.font.SysFont('times new roman', 20)
    score_surface = score_font.render('Leader score : ' + str(score), True, white)
    max_surface = score_font.render('Max score : ' + str(max_score), True, white)
    display.blit(score_surface, [dis_width // 4 * 0 + 2 * pad, pad // 4, pad, 25])
    display.blit(max_surface, [dis_width // 4 * 3 + 2 * pad, pad // 4, pad, 25])

    if not generation is None:
        generation_surface = score_font.render('Generation : ' + str(generation), True, white)
        epsilon_surface = score_font.render('Epsilon : ' + '{:.6f}'.format(epsilon), True, white)
        display.blit(generation_surface, [dis_width // 4 + 2 * pad, pad // 4, pad, 25])
        display.blit(epsilon_surface, [dis_width // 2 + 2 * pad, pad // 4, pad, 25])

    return start_position


def draw_snake(snake, start):
    head = snake.body[0]
    pygame.draw.rect(display, snake.color_head,
                     [head[0] * size_block + border + start[0], head[1] * size_block + border + start[1],
                      snake_block, snake_block])
    for x in snake.body[1:]:
        pygame.draw.rect(display, snake.color,
                         [x[0] * size_block + border + start[0], x[1] * size_block + border + start[1],
                          snake_block, snake_block])


def draw_food(food, start):
    pygame.draw.rect(display, food.color,
                     [food.x * size_block + border + start[0], food.y * size_block + border + start[1], snake_block,
                      snake_block])


def action_snake(action, pre_action):
    res = None
    if pre_action == pygame.K_RIGHT:
        if action == 0:
            res = pygame.K_UP
        elif action == 1:
            res = pygame.K_RIGHT
        else:
            res = pygame.K_DOWN
    if pre_action == pygame.K_LEFT:
        if action == 0:
            res = pygame.K_DOWN
        elif action == 1:
            res = pygame.K_LEFT
        else:
            res = pygame.K_UP
    if pre_action == pygame.K_UP:
        if action == 0:
            res = pygame.K_LEFT
        elif action == 1:
            res = pygame.K_UP
        else:
            res = pygame.K_RIGHT
    if pre_action == pygame.K_DOWN:
        if action == 0:
            res = pygame.K_RIGHT
        elif action == 1:
            res = pygame.K_DOWN
        else:
            res = pygame.K_LEFT
    return res