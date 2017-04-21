__author__ = 'Eshin Kunishima'
__license__ = 'MIT'

from PIL import Image

from forest import Forest

wood = Image.open('tile/wood.png')
bamboo = Image.open('tile/bamboo.png')
fire = Image.open('tile/fire.png')
soil = Image.open('tile/soil.png')
pool = Image.open('tile/pool.png')
road = Image.open('tile/road.png')
mountain = Image.open('tile/mountain.png')


def forest2bmp(forest: Forest, filename: str):
    bmp = Image.new('RGB', (forest.x * 32, forest.y * 32), (255, 255, 255))
    for y in range(forest.y):
        for x in range(forest.x):
            cell = str(forest.get_cell(x, y))
            dx = x * 32
            dy = y * 32

            if cell == 'W':
                bmp.paste(wood, (dx, dy))
            elif cell == 'B':
                bmp.paste(bamboo, (dx, dy))
            elif cell == 'F':
                bmp.paste(fire, (dx, dy))
            elif cell == 'S':
                bmp.paste(soil, (dx, dy))
            elif cell == 'P':
                bmp.paste(pool, (dx, dy))
            elif cell == 'R':
                bmp.paste(road, (dx, dy))
            elif cell == 'M':
                bmp.paste(mountain, (dx, dy))

    bmp.save(filename, 'PNG')


f = Forest()
f.loads(open('default.txt', mode='r').read())
forest2bmp(f, 'r_0.png')
for t in range(24 * 7):
    f.next_generation()
    forest2bmp(f, 'r_%d.png' % (t + 1))
