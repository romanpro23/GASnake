from genetic_algoritm.snake_gaV1 import SnakeAI
import random
import torch


class Population:
    def __init__(self, size, height=30, width=40, mutation_rate=0.01):
        self.size = size
        self.snakes = [SnakeAI(3, height, width) for _ in range(size)]
        self.counter = 0
        self.mutation_rate = mutation_rate

    def get_subpopulation(self, size):
        if self.counter >= self.size:
            self.counter = 0
        subpopulation = self.snakes[self.counter:min(self.counter + size, self.size)]
        self.counter += size
        return subpopulation

    def crossover(self):
        fitness = self.selection()
        new_population = []
        for _ in range(self.size):
            child = self._recombination(self.snakes[random.choice(fitness)], self.snakes[random.choice(fitness)])
            new_population.append(child)

        self.snakes = new_population

    def _recombination(self, snake_m, snake_f):
        child = SnakeAI(3, snake_m.height, snake_m.width)
        self._phenotype(child, snake_m, snake_f)
        brain = child.brain.brain
        for c, m, f in zip(brain.parameters(), snake_m.brain.brain.parameters(), snake_f.brain.brain.parameters()):
            self._crossover(c, m, f)
            self._mutation(c)

        return child

    def _phenotype(self, c, m, f):
        rm, gm, bm = m.color_head
        rf, gf, bf = f.color_head
        rand = random.random()
        rang = (1 - self.mutation_rate) / 3
        if rand < rang:
            c.color_head = (rm, gm, bm)
        elif rang <= rand < rang*2:
            c.color_head = (rf, gf, bf)
        elif rang * 2 <= rand < rang * 3:
            c.color_head = ((rm + rf) / 2, (gm + gf) / 2, (bm + bf) / 2)
        else:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            c.color_head = (r, g, b)

    def _crossover(self, c, m, f):
        with torch.no_grad():
            mask = torch.rand_like(c) < 0.5
            c[mask] = m[mask]
            c[~mask] = f[~mask]

    def _crossover_onpnt(self, c, m, f):
        with torch.no_grad():
            rand_p = torch.randint(0, m.shape[0], (1,))
            mask = torch.cat([i < rand_p for i in range(m.shape[0])])
            c[mask] = m[mask]
            c[~mask] = f[~mask]

    def _crossover_avg(self, c, m, f):
        with torch.no_grad():
            c[...] = (m + f) / 2

    def _mutation(self, c):
        with torch.no_grad():
            mask = torch.rand_like(c) < self.mutation_rate
            max_v = torch.max(c)
            min_v = torch.min(c)
            range_v = max_v - min_v
            rand = range_v * torch.rand_like(c) + min_v
            c[mask] = rand[mask]

    def selection(self):
        count_score = sum(snake.fitness_score for snake in self.snakes) / 100
        fitness = [i for i, snake in enumerate(self.snakes) for _ in range(int(snake.fitness_score / count_score))]
        # fitness = [i for i, snake in enumerate(self.snakes) for _ in range(snake.score if snake.score > 1 else 0)]
        # fitness = [i for i, snake in enumerate(self.snakes) for _ in range(snake.score * 10 if snake.score > 0 else 1)]
        print(count_score)
        return fitness
