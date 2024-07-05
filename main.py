import random

import pygame as pg


def get_cells(image, count):
    images = []
    cells = []

    for i in range(count):
        x = (i * N) % (N * N)
        y = (i * N) // (N * N)
        images.append(image.subsurface((x, y, N, N)))

    for img in images:
        cell = Cell(img)
        cell.neighbours(images)
        cells.append(cell)

    return cells


class Map:
    def __init__(self):
        image = pg.image.load("Maze.png")
        w, h = image.get_size()
        count = (w * h) // (N * N)
        self.cells = []
        self._get_cells(image, count)

        self.map_list = [[None] * COUNT_X for _ in range(COUNT_Y)]
        self.wave = [[[True] * count] * COUNT_X for _ in range(COUNT_Y)]
        self.entropy = []
        for row in self.wave:
            ent_row = [sum(q) for q in row]
            self.entropy.append(ent_row)
        self.finish = False
        self.image = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def update_entropy(self):
        for y in range(COUNT_Y):
            for x in range(COUNT_X):
                self.entropy[y][x] = sum(self.wave[y][x])

    def update_image(self):
        for y, row in enumerate(self.map_list):
            for x, cell in enumerate(row):
                if cell is not None:
                    img = pg.transform.scale_by(self.cells[cell].image, SCALE // N)
                    self.image.blit(img, (x * SCALE, y * SCALE))

    def _get_cells(self, image, count):
        images = []

        for i in range(count):
            x = (i * N) % (N * N)
            y = (i * N) // (N * N)
            images.append(image.subsurface((x, y, N, N)))

        for img in images:
            cell = Cell(img)
            cell.neighbours(images)
            self.cells.append(cell)

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

    def update(self):
        for i in range(COUNT_X * COUNT_Y):
            x_n, y_n = random.randint(0, COUNT_X - 1), random.randint(0, COUNT_Y - 1)
            if self.map_list[y_n][x_n] is None and self.entropy[y_n][x_n] != 0:
                break
        else:
            self.finish = True
        min_ent = len(self.cells)
        for y, row in enumerate(self.entropy):
            for x, ent in enumerate(row):
                if 0 < ent <= min(row):
                    x_n, y_n = x, y
                    min_ent = ent
        if not self.finish:
            a = list(range(len(self.cells)))
            random.shuffle(a)
            n = random.randint(0, len(self.cells) - 1)
            for i in a:
                if self.wave[y_n][x_n][i]:
                    n = i
                    break

            self.map_list[y_n][x_n] = n
            self.wave[y_n][x_n] = [False] * len(self.cells)

            for i in range(len(self.cells)):
                self.wave[y_n][(x_n - 1) % COUNT_X][i] = self.wave[y_n][(x_n - 1) % COUNT_X][i] and self.cells[n].left[i]
                self.wave[y_n][(x_n + 1) % COUNT_X][i] = self.wave[y_n][(x_n + 1) % COUNT_X][i] and self.cells[n].right[i]
                self.wave[(y_n + 1) % COUNT_Y][x_n][i] = self.wave[(y_n + 1) % COUNT_Y][x_n][i] and self.cells[n].bottom[i]
                self.wave[(y_n - 1) % COUNT_Y][x_n][i] = self.wave[(y_n - 1) % COUNT_Y][x_n][i] and self.cells[n].top[i]

            self.update_image()
            self.update_entropy()


class Cell:
    def __init__(self, image: pg.Surface):
        self.image = image
        self.left = []
        self.right = []
        self.top = []
        self.bottom = []

    def neighbours(self, cells):
        for cell in cells:
            left = True
            right = True
            top = True
            bottom = True
            for i in range(N):
                if self.image.get_at((N - 1, i)) != cell.get_at((0, i)):
                    right = False
                if self.image.get_at((0, i)) != cell.get_at((N - 1, i)):
                    left = False
                if self.image.get_at((i, 0)) != cell.get_at((i, N - 1)):
                    top = False
                if self.image.get_at((i, N - 1)) != cell.get_at((i, 0)):
                    bottom = False
            self.left.append(left)
            self.right.append(right)
            self.top.append(top)
            self.bottom.append(bottom)


# Screen settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
FPS = 60
N = 4
SCALE = 32
COUNT_X = SCREEN_WIDTH // SCALE
COUNT_Y = SCREEN_HEIGHT // SCALE

# Initialize window
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Generation')

# Game loop settings

running = True
clock = pg.time.Clock()

level = Map()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    level.update()
    level.draw(screen)

    dt = clock.tick(FPS) / 1000
    pg.display.update()

pg.quit()
