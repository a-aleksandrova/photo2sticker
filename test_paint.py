import pygame as pg

imageName = "target.jpg"
image = pg.image.load(imageName)
width, height = image.get_rect().size
screen = pg.display.set_mode((width, height))
canvas = screen.copy()

draw_on = False
last_pos = (0, 0)
radius = 6

def roundline(srf, color, start, end, radius=1):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pg.draw.circle(srf, color, (x, y), radius)

#    Цвета            R    G    B
BLACK = pg.Color( 0 ,  0 ,  0 )
WHITE = pg.Color(255, 255, 255)
BLUE  = pg.Color( 0 , 128, 255)
KEY   = pg.Color(100,  0 , 255)
ORANGE= pg.Color(255, 128,  0 )

color = ORANGE
canvas.fill(KEY)
canvas.set_colorkey(KEY)
canvas.set_alpha(150)
mode = True
done = False
while not done:
    event = pg.event.wait()
    if event.type == pg.QUIT:
        done = True
    if event.type == pg.MOUSEBUTTONDOWN:
        pg.draw.circle(canvas, color, event.pos, radius)
        draw_on = True
    if event.type == pg.MOUSEBUTTONUP:
        draw_on = False
    if event.type == pg.MOUSEMOTION:
        if event.buttons[0] == 1:
            if mode == True:
                color = ORANGE
            else:
                color = BLUE
        elif event.buttons[2] == 1:
            color = KEY
        if draw_on:
            pg.draw.circle(canvas, color, event.pos, radius)
            roundline(canvas, color, event.pos, last_pos, radius)
        last_pos = event.pos
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_s:         # "s"    - сохраняет цветную маску
            pg.image.save(canvas, "canvas.png")
        if event.key == pg.K_LALT:      # "lalt" - меняет режим
            mode = not mode
        if event.key == pg.K_EQUALS:    # "="(+) - увеличивает радиус
            radius += 1
        elif event.key == pg.K_MINUS:   # "-"    - уменьшает радиус
            if radius > 1:
                radius -= 1
    screen.blit(image, (0, 0))
    screen.blit(canvas, (0, 0))
    pg.display.flip()

pg.quit()
