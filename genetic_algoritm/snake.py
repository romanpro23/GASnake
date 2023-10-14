class Snake:
    def __init__(self, length, height, width):
        self.height = height
        self.width = width
        self.start_length = length
        self.new()

    def new(self):
        x0 = self.width // 2 + self.start_length
        y0 = self.height // 2
        self.length = self.start_length
        self.body = [(x0 - i, y0) for i in range(self.start_length)]

        self.color = (255, 255, 255)
        self.color_head = (0, 255, 100)
        self.score = 0

        self.dx = 0
        self.dy = 0

    def _check_wall(self):
        x0, y0 = self.body[0]
        return x0 >= self.width or x0 < 0 or y0 >= self.height or y0 < 0

    def _check_self(self):
        x0, y0 = self.body[0]
        for x, y in self.body[1:]:
            if x == x0 and y == y0:
                return True
        return False

    def _repaint(self):
        r, g, b = self.color
        if r > 127:
            self.color = (r - 1, g - 1, b - 1)

    def _check_food(self, food):
        for x, y in self.body:
            if x == food.x and y == food.y:
                return True
        return False

    def _eat_food(self, food):
        self.score += food.rate
        while self._check_food(food):
            food.new()

        self.length += 1
        self._repaint()

    def move(self, dx, dy):
        self.dx = dx
        self.dy = dy
        x0, y0 = self.body[0]
        if not self.dx == 0 or not self.dy == 0:
            self.body = [(x0 + dx, y0 + dy)] + self.body

    def ate(self, foods):
        x0, y0 = self.body[0]
        ate = False
        reward = 0
        for food in foods:
            if x0 == food.x and y0 == food.y:
                self._eat_food(food)
                ate = True
                reward = food.rate
                break
        if not ate and (not self.dx == 0 or not self.dy == 0):
            self.body = self.body[:-1]

        return reward

    def check_die(self):
        return self._check_wall() or self._check_self()
