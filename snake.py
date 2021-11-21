import random
import time
import pygame as pg

pg.init()

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

screen = pg.display.set_mode((600, 600))
pg.display.set_caption('SNAKE')


def col(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])


def apple_position():
    return random.randint(0, 580) // 10 * 10, random.randint(0, 580) // 10 * 10


big_apple_pos = (-10, -10)
big_apple_sur = pg.Surface((10, 10))
big_apple_sur.fill((0, 0, 255))

snake = [(200, 200), (210, 200), (220, 200)]

apple_pos = apple_position()
apple_sur = pg.Surface((10, 10))
apple_sur.fill((255, 0, 0))

direction = LEFT
clock = pg.time.Clock()

s = pg.Surface((10, 10))
s.fill((255, 255, 255))

font = pg.font.Font('freesansbold.ttf', 18)
score = 0
tick = 10
level = 1
clevel = 1
r = 0
g = 0
b = 0

print("Digite o seu nome: ")
name = input()


def scoreboard():
    players = [(score, name)]
    try:
        f = open("scoreboard.txt", "r")
        for line in f:
            user_info = line.strip().split(" ")
            players.append((int(user_info[1]), user_info[0]))
        f.close()

        players.sort(key=lambda x: (-x[0], x[1]))

        print("-----LEADERBOARD-----")
        if len(players) == 1:
            print(f"1º-{players[0][1]}: {players[0][0]}")
        elif len(players) == 2:
            for t in range(len(players)):
                print(f"{t + 1}º-{players[t][1]}: {players[t][0]}")
        elif len(players) == 3:
            for th in range(len(players)):
                print(f"{th + 1}º-{players[th][1]}: {players[th][0]}")
        elif len(players) == 4:
            for f in range(len(players)):
                print(f"{f + 1}º-{players[f][1]}: {players[f][0]}")
        elif len(players) >= 5:
            for fi in range(5):
                print(f"{fi + 1}º-{players[fi][1]}: {players[fi][0]}")

        f1 = open("scoreboard.txt", "a")
        f1.write(f"{name} {score}\n")
        f1.close()

    except NameError:
        print("erro no ficheiro")


time.sleep(3)
while True:

    clock.tick(tick)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            scoreboard()
            pg.quit()
            exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and direction != DOWN:
                direction = UP
            if event.key == pg.K_DOWN and direction != UP:
                direction = DOWN
            if event.key == pg.K_RIGHT and direction != LEFT:
                direction = RIGHT
            if event.key == pg.K_LEFT and direction != RIGHT:
                direction = LEFT

    screen.fill((r, g, b))
    screen.blit(apple_sur, apple_pos)
    screen.blit(big_apple_sur, big_apple_pos)

    scorefont = font.render('Score %s' % score, True, (255, 255, 255))
    scorearea = scorefont.get_rect()
    scorearea.topleft = (600 - 120, 10)
    screen.blit(scorefont, scorearea)

    scoreLevel = font.render('Level %s' % level, True, (255, 255, 255))
    scorearea2 = scorefont.get_rect()
    scorearea.topright = (0, 10)
    screen.blit(scoreLevel, scorearea2)

    if snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0:
        scoreboard()
        pg.quit()
        exit()

    for i in range(1, len(snake) - 1):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            scoreboard()
            pg.quit()
            exit()

    if col(snake[0], big_apple_pos):
        for i in range(10):
            snake.append((0, 0))
        apple_pos = apple_position()
        big_apple_pos = (-10, -10)

        for i in range(10):
            score = score + 1
            if score % 5 == 0:
                tick = tick + 1
                level = level + 1

    if col(snake[0], apple_pos):
        rand = random.randint(0, 100)
        if rand < 10:
            big_apple_pos = apple_position()
            apple_pos = (-10, 10)
        elif rand > 10:
            apple_pos = apple_position()
        snake.append((0, 0))
        score = score + 1

        if score % 5 == 0:
            tick = tick + 1
            level = level + 1

    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i - 1][0], snake[i - 1][1])

    if direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - 10)
    if direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 10)
    if direction == RIGHT:
        snake[0] = (snake[0][0] + 10, snake[0][1])
    if direction == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1])

    if level - clevel >= 2:
        clevel = level

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        sr = random.randint(0, 255)
        sg = random.randint(0, 255)
        sb = random.randint(0, 255)

        while r - sr >= 50 and g - sg >= 50 and b - sb >= 50 or \
                r >= 230 and g <= 80 and b <= 80 or r <= 80 and g <= 80 and b >= 230:
            print("recolorir")
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)

            sr = random.randint(0, 255)
            sg = random.randint(0, 255)
            sb = random.randint(0, 255)

        s.fill((sr, sg, sb))

    for pos in snake:
        screen.blit(s, pos)

    pg.display.update()
