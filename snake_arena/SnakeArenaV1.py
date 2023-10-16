from snake_arena.food import Food
from snake_arena.snake_arena_game import *
from genetic_algoritm.population import *

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
        epsilon_surface = score_font.render('Mutation rate : ' + '{:.6f}'.format(epsilon), True, white)
        display.blit(generation_surface, [dis_width // 4 + 2 * pad, pad // 4, pad, 25])
        display.blit(epsilon_surface, [dis_width // 2 + 2 * pad, pad // 4, pad, 25])

    return start_position

snake_speed=1000

def gameLoop():
    pygame.display.update()
    game_over = False

    count = count_h * count_w
    dx = [0] * count
    dy = [0] * count

    preEvent = [pygame.K_RIGHT] * count
    game_end = [False] * count
    reward_counter = [0] * count
    count_subpopulation = 20
    population = Population(count * count_subpopulation, mutation_rate=0.01)
    snakes = []
    foods = [Food(h, w) for _ in range(count)]

    # for i in range(boards[2].shape[0]):
    #     for j in range(boards[2].shape[1]):
    #         print(boards[2][i][j], end=" ")
    #     print()
    max_score = 0
    generation = 0
    population_alive = True
    subpopulation_alive = False
    counter_subpopulation = 0
    boards = []
    epsilon = population.mutation_rate
    max_count_step = [70] * count

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
        display.fill(black)

        if not population_alive:
            population.crossover()
            generation += 1
            population_alive = True

            # generation % 20:
            #     max_reward += 50
        if not subpopulation_alive:
            if counter_subpopulation == count_subpopulation:
                counter_subpopulation = 0
                population_alive = False
                subpopulation_alive = False
                continue
            snakes = population.get_subpopulation(count)
            boards = [make_board(snake, [food], []) for snake, food in zip(snakes, foods)]
            counter_subpopulation += 1
            subpopulation_alive = True

        # print(counter_subpopulation)
        leader_score = np.max([snake.score for snake in snakes])
        position = draw_borders(leader_score, epsilon, max_score, generation=generation)

        if not False in game_end:
            preEvent = [pygame.K_RIGHT] * count
            game_end = [False] * count
            reward_counter = [0] * count
            max_count_step = [70] * count
            subpopulation_alive = False
            continue

        for i in range(count):
            head_x, head_y = snakes[i].body[0]

            if not game_end[i]:
                snake = snakes[i]
                food = foods[i]
                draw_food(food, position[i])
                draw_snake(snake, position[i])

                action = snake.action(boards[i], food)
                action = action_snake(action, pre_action=preEvent[i])

                if action == pygame.K_LEFT and not preEvent[i] == pygame.K_RIGHT:
                    dx[i] = -1
                    dy[i] = 0
                    preEvent[i] = action
                elif action == pygame.K_RIGHT and not preEvent[i] == pygame.K_LEFT:
                    dx[i] = 1
                    dy[i] = 0
                    preEvent[i] = action
                elif action == pygame.K_UP and not preEvent[i] == pygame.K_DOWN:
                    dy[i] = -1
                    dx[i] = 0
                    preEvent[i] = action
                elif action == pygame.K_DOWN and not preEvent[i] == pygame.K_UP:
                    dy[i] = 1
                    dx[i] = 0
                    preEvent[i] = action

                snake.move(dx[i], dy[i])
                food_x, food_y = foods[i].x, foods[i].y
                reward = snake.ate([food]) * 10
                game_end[i] = snake.check_die()

                if reward == 0:
                    reward_counter[i] += 1
                else:
                    max_count_step[i] += 1
                    reward_counter[i] = 0

                    fitness_score = (1200 - (reward_counter[i] - (abs(head_x - food_x) + abs(head_y - food_y)))) / (1200 / len(snake.body))
                    snake.fitness_score += fitness_score
                    head_x, head_y = snakes[i].body[0]

                if reward_counter[i] > max_count_step[i]:
                    game_end[i] = True
                    reward_counter[i] = 0
                boards[i] = make_board(snake, [food], [])
                if game_end[i]:
                    dx[i] = 0
                    dy[i] = 0
                    preEvent[i] = pygame.K_RIGHT
                    food.new()
                    if max_score < snake.score:
                        max_score = snake.score
                        snake.brain.save(f"D://Python//SnakeAI//snake_brain//brain_gav1")

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()


if __name__ == '__main__':
    gameLoop()

