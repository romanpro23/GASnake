import random

class Food:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.x = round(random.randrange(0, width-1))
        self.y = round(random.randrange(0, height-1))
        if self.y == height // 2:
            self.y += random.randrange(2, 5)

        self.color = (255, 10, 10)
        self.rate = 1

    def _make(self):
        rand = random.randint(0, 100)
        if (rand < 85):
            self.color = (255, 10, 10)
        elif (rand < 95 and rand >= 85):
            self.color = (255, 100, 10)
        elif (rand > 95):
            self.color = (255, 50, 10)

    def new(self):
        self._make()
        self.x = round(random.randrange(0, self.width - 1))
        self.y = round(random.randrange(0, self.height - 1))

