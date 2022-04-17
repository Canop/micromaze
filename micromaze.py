from microbit import *
import music

# the + is the starting position and the o are the treasures
MAZE = ("████████████████████████████████████████:"
        "█    █           █o    █  █o█ █       o█:"
        "██ █ █ o█o███o█  ██  █ █    █o█ ████████:"
        "█o █ ██████o███   █ ██ ██ █   █ █ o█   █:"
        "████            █   o█    █ ███ █ ██ █ █:"
        "█o █████████ ████████████ █ █   █  █ █ █:"
        "█          █  █o █     █o █ █ ████ █ █o█:"
        "███ █████o ██    █ + █ █    █ █    █ ███:"
        "█   █      █o █     o█    █ █ █ ██     █:"
        "█ ███ █ █ o██████████████ █o█ █ █  ███ █:"
        "█   █ █o█                 ███ █ █o█ o█ █:"
        "███ █ █████████████████████   █o███ ██ █:"
        "█o                          █          █:"
        "████████████████████████████████████████:")

WALL = 4
PLAYER = 7
TREASURE = 1
TREASURE_BLINK = 6

PICK_TUNE = ["C4:2", "D4:1", "E4:3"]

IPX = 5
IPY = 5
treasures = 0
maze = Image(
    MAZE
        .replace(" ", "0")
        .replace("+", str(PLAYER))
        .replace("o", str(TREASURE))
        .replace("█", str(WALL))
)
W = maze.width()
H = maze.height()
for x in range(W):
    for y in range(H):
        if maze.get_pixel(x, y) == TREASURE:
            treasures += 1
        if maze.get_pixel(x, y) == PLAYER:
            maze.set_pixel(x, y, 0)
            IPX = x
            IPY = y

# screen pos in the maze ref
sx = 0
sy = 0

# player pos
px = IPX
py = IPY

count = 0

def pix(x, y):
    global maze
    maze.set_pixel(x, y, 2)
def hline(x, y, dx):
    global maze
    for i in range(dx):
        if x + i < W:
            maze.set_pixel(x + i, y, 2)
def vline(x, y, dy):
    global maze
    for i in range(dy):
        if y + i < H:
            maze.set_pixel(x, y + i, 2)
def rect(x, y, dx, dy):
    hline(x, y, dx)
    hline(x, y+dy-1, dx)
    vline(x, y, dy)
    vline(x+dx-1, y, dy)

def show():
    global maze, sx, sy, px, py
    scr = Image(5, 5)
    scr.blit(maze, sx, sy, 5, 5)
    scr.set_pixel(px - sx, py - sy, PLAYER)
    if count%2 == 1:
        for x in range(5):
            for y in range(5):
                if scr.get_pixel(x, y) == TREASURE:
                    scr.set_pixel(x, y, TREASURE_BLINK)
    display.show(scr)

def be_off():
    music.play(music.POWER_DOWN)
    display.clear()
    while True:
        if button_b.is_pressed():
            music.play(music.POWER_UP)
            break

def can_go(x, y):
    global maze
    return maze.get_pixel(x, y) != WALL

def update():
    global maze, sx, sy, px, py, count, treasures
    count += 1
    ax = accelerometer.get_x()
    ay = accelerometer.get_y()
    vx = 0
    vy = 0
    if ax > 70:
        vx = 1
    elif ax < -70:
        vx = -1
    if ay > 70:
        vy = 1
    elif ay < -70:
        vy = -1
    if can_go(px+vx, py+vy):
        px += vx
        py += vy
    elif can_go(px+vx, py):
        px += vx
    elif can_go(px, py+vy):
        py += vy
    if maze.get_pixel(px, py) == TREASURE:
        show()
        maze.set_pixel(px, py, 0)
        treasures -= 1
        music.play(PICK_TUNE)
        display.scroll(str(treasures))
    if px - sx < 1:
        sx -= 1
    elif px - sx > 3:
        sx += 1
    if py - sy < 1:
        sy -= 1
    elif py - sy > 3:
        sy += 1

def is_win():
    global treasures
    return treasures == 0

def start(): # go back to initial position
    global px, py, IPX, IPY, sx, sy
    px = IPX
    py = IPY
    sx = px - 2
    sy = py - 2
    music.play(music.DADADADUM)
    display.scroll(str(treasures))
    show()

def on_win():
    display.show(Image.HAPPY)
    while True:
        if button_a.is_pressed():
            start()
            break
        if button_b.is_pressed():
            be_off()

start()
be_off()
while True: # MAIN LOOP
    sleep(200)
    if button_a.is_pressed():
        start()
    if button_b.is_pressed():
        be_off()
    update()
    show()
    if is_win():
        on_win()

