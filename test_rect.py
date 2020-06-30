import pygame as pg
filename = "target.jpg"
def get_rects():
    pg.init()
    image = pg.image.load(filename)
    width, height = image.get_rect().size
    window = pg.display.set_mode((width, height))
    rect = pg.Rect(100, 100, 161, 100)
    rect_selected = False

    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                # Изменить rect_selected на True когда нажатие происходит внутри прямоугольника.
                if rect.collidepoint(event.pos):
                    rect_selected = True
            elif event.type == pg.MOUSEBUTTONUP:
                rect_selected = False
            elif event.type == pg.MOUSEMOTION:
                if rect_selected:
                    if pg.mouse.get_pressed()[2] == 1: # Правая кнопка мыши нажата
                        # Изменить ширину и высоту прямоугольника относительно движения мыши.
                        rect.w += event.rel[0]
                        rect.h += event.rel[1]
                        # 10 на 10 минимальный размер
                        rect.w = max(rect.w, 10)
                        rect.h = max(rect.h, 10)
                    if pg.mouse.get_pressed()[0] == 1: # Левая кнопка мыши нажата
                        # Переместить прямоугольник за мышью.
                        rect.x += event.rel[0]
                        rect.y += event.rel[1]
        window.blit(image, (0, 0))
        pg.draw.rect(window, (0, 100, 250), rect, 2)
        pg.display.flip()
    return rect[0], rect[1], rect[0]+rect[2], rect[1]+rect[3] #Возвращает координаты углов
print(get_rects())
