import pygame as pg


def get_entropy():
    entropy = []
    for row in wave:
        ent_row = [sum(q) for q in row]
        entropy.append(ent_row)
    return entropy


def draw_map():
    surf = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for y, row in enumerate(map_list):
        for x, cell in enumerate(row):
            if cell is not None:
                img = pg.transform.scale_by(cells[cell].image, SCALE // N)
                surf.blit(img, (x * SCALE, y * SCALE))
            # img = pg.transform.scale_by(cells[1].image, SCALE / N)
            # surf.blit(img, (x * SCALE, y * SCALE))

    return surf


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
                if self.image.get_at((3, i)) != cell.get_at((0, i)):
                    right = False
                if self.image.get_at((0, i)) != cell.get_at((3, i)):
                    left = False
                if self.image.get_at((i, 0)) != cell.get_at((i, 3)):
                    top = False
                if self.image.get_at((i, 3)) != cell.get_at((i, 0)):
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

# Initialize window

pg.init()

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pg.display.set_caption('Generation')

# Game loop settings

running = True
image = pg.image.load("Maze.png")
# image = pg.transform.scale_by(image, SCALE)
w, h = image.get_size()
count = (w * h) // (N * N)
cells = get_cells(image, count)
clock = pg.time.Clock()

wave = []
map_list = []

for i in range(SCREEN_HEIGHT // SCALE):
    row = []
    row_map = []
    for j in range(SCREEN_WIDTH // SCALE):
        row.append([True] * count)
        row_map.append(None)
    wave.append(row)
    map_list.append(row_map)

print(len(wave))
entropy = get_entropy()

print(entropy)

map_image = draw_map()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    min_ent = count
    x_n, y_n = 0, 0

    for y, row in enumerate(entropy):
        for x, ent in enumerate(row):
            if 0 < ent <= min_ent:
                min_ent = ent
                x_n, y_n = x, y
    n = wave[y_n][x_n].index(True)
    map_list[y_n][x_n] = n

    wave[y_n][x_n - 1] = wave[y_n][x_n - 1] and cells[n].left
    map_image = draw_map()
    screen.blit(map_image, (0, 0))
    dt = clock.tick(FPS) / 1000
    pg.display.update()

pg.quit()
