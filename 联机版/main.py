"""
这可能不是一个游戏.This may not be a game.
MADE BY Wotemo.
"""

import pygame
import random
import sys
import requests

pygame.init()

window_width, window_height = 600, 600

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('贪吃蛇 | Wotemo')
icon = pygame.image.load('resources/snake.ico')
pygame.display.set_icon(icon)

pygame.mixer.music.load('resources/bgmusic.mp3')
pygame.mixer.music.play(-1)

font_source = 'resources/君子怀旧仿宋体.ttf'

window.fill((229, 231, 206))
pygame.display.flip()


def draw_bg():
    """画背景"""
    line_height = 75
    line_width = 0
    while line_height <= window_height:
        pygame.draw.line(window, (0, 0, 0), (0, line_height), (window_width, line_height))
        line_height += 25
    while line_width <= window_width:
        pygame.draw.line(window, (0, 0, 0), (line_width, 75), (line_width, window_height))
        line_width += 25


def fonts(font_pos, content, font_style, is_true, font_color, font_size):
    """便捷生成字体的函数"""
    # 以上分别对应：文字显示位置()元组，
    # 文字内容''字符串，
    # 字体样式''字符串路径，
    # 是否是平滑字体True布尔值，
    # 字体颜色()元组，
    # 字体大小1整数
    fonts_temp = pygame.font.Font(font_style, font_size)
    window.blit(fonts_temp.render(content, is_true, font_color), font_pos)
    pygame.display.update()


def fonts_mid(font_pos, content, font_style, is_true, font_color, font_size):
    """便捷生成字体的函数"""
    # 以上分别对应：文字显示位置()元组，
    # 文字内容''字符串，
    # 字体样式''字符串路径，
    # 是否是平滑字体True布尔值，
    # 字体颜色()元组，
    # 字体大小1整数
    fonts_temp = pygame.font.Font(font_style, font_size)
    fonts_temp_two = fonts_temp.render(content, is_true, font_color)
    font_pos_temp = fonts_temp_two.get_size()
    w = font_pos_temp[0]
    h = font_pos_temp[1]
    w_mid = (window_width - w) / 2
    h_mid = (window_height - h) / 2
    if type(font_pos[0]) == int:
        w_mid = font_pos[0]
    if type(font_pos[1]) == int:
        h_mid = font_pos[1]
    font_pos_final = (w_mid, h_mid)
    window.blit(fonts_temp_two, font_pos_final)
    pygame.display.update()


import InputBox
fonts_mid((False,200), '请输入您的用户名', font_source, True, (47, 125, 242), 25)
userinputs = InputBox.main()
window.fill((229, 231, 206))
draw_bg()

def user_submit():
    un = userinputs[0]
    if __name__ == '__main__':
        window.fill((229, 231, 206))
        fonts_mid((False, 200), '稍等', font_source, True, (32, 45, 82), 25)
        url = 'http://39.105.170.197:5000/login'
        data = {'username': un}
        r = requests.post(url, data=data)
        # 打印响应时间单位s
        r_time = r.elapsed.microseconds / 1000000
        # 打印响应结果
        r_text = r.text
        print(f'你的分数为：{r_text} 用时：{r_time}')
        return r.text

try:
    score_int = int(user_submit())
    pygame.time.wait(600)
except:
    score_int = 0
window.fill((229, 231, 206))
scores = pygame.font.Font(font_source, 50).render(str(score_int), True, (66, 133, 244))
score_w, score_h = scores.get_size()
score_ws = (window_width - score_w) / 2
score_hs = (75 - score_h) / 2
window.blit(scores, (score_ws, score_hs))
pygame.display.update()

fonts((0, 12), 'SCORE:', font_source, True, (66, 133, 244), 50)
# fonts((300, 12), str(score_int), font_source, True, (66, 133, 244), 50)
draw_bg()

rw = random.randrange(25, 575, 25)
rh = random.randrange(100, 575, 25)

# rwc = random.randrange(25, 575, 25)
# rhc = random.randrange(100, 575, 25)


rwhcs = []
# while candy_num <3:
#     rwc = random.randrange(25, 575, 25)
#     rhc = random.randrange(100, 575, 25)
#     rwhc = (rwc, rhc)
#     rwhcs.append(rwhc)
#     candy_num += 1


def creat_candy(num):
    candy_num = 0
    while candy_num < num:
        rwc = random.randrange(25, 575, 25)
        rhc = random.randrange(100, 575, 25)
        rwhc = (rwc, rhc)
        if rwhc in rwhcs:
            pass
        else:
            rwhcs.append(rwhc)
            candy_num += 1


creat_candy(3)  # 创建初始糖果

print(f'初始糖果位置{rwhcs}')

# snake = pygame.draw.rect(window, (118, 37, 39), (rw, rh, 25, 25))
# candy = pygame.draw.rect(window, (1, 185, 237), (rwc, rhc, 25, 25))
# pygame.display.update()


active = 0
active_time = 0
speed = 100
while True:

    window.fill((229, 231, 206), (rw, rh, 25, 25))

    snake_pos = (rw, rh)

    if snake_pos in rwhcs:
        snake_index = rwhcs.index(snake_pos)
        rwc = random.randrange(25, 575, 25)
        rhc = random.randrange(100, 575, 25)
        rwhc = (rwc, rhc)
        rwhcs[snake_index] = rwhc

        pygame.mixer.Sound('resources/eat.mp3').play(0)

        pygame.draw.rect(window, (1, 185, 237), (rw, rh, 25, 25))
        pygame.display.update()

        if score_int < 500:
            score_int += 100
            speed = 95
        if 500 <= score_int < 1000:
            score_int += 100
            speed = 90
            if len(rwhcs) <= 3:
                creat_candy(1)
        if 1000 <= score_int < 1500:
            score_int += 150
            speed = 85
            if len(rwhcs) <= 4:
                creat_candy(1)
        if 1500 <= score_int < 2000:
            score_int += 200
            speed = 80
            if len(rwhcs) <= 5:
                creat_candy(1)
        if 2000 <= score_int < 2500:
            score_int += 250
            speed = 75
            if len(rwhcs) <= 6:
                creat_candy(1)
        if 2500 <= score_int < 3000:
            score_int += 300
            speed = 70
            if len(rwhcs) <= 7:
                creat_candy(1)
        if 3000 <= score_int:
            score_int += 350
            speed = 65
            if len(rwhcs) <= 8:
                creat_candy(1)

        if score_int <= 999999:
            window.fill((229, 231, 206), (180, 0, 420, 75))

            scores = pygame.font.Font(font_source, 50).render(str(score_int), True, (66, 133, 244))
            score_w, score_h = scores.get_size()
            score_ws = (window_width - score_w) / 2
            score_hs = (75 - score_h) / 2
            window.blit(scores, (score_ws, score_hs))
        else:
            window.fill((229, 231, 206), (180, 0, 420, 75))
            scores = pygame.font.Font(font_source, 50).render('999999+', True, (66, 133, 244))
            score_w, score_h = scores.get_size()
            score_ws = (window_width - score_w) / 2
            score_hs = (75 - score_h) / 2
            window.blit(scores, (score_ws, score_hs))
        print(f'得分{score_int}')


    if rw in [0, 575] or rh in [75, 575]:
        active = 0
        pygame.mixer.Sound('resources/gameover.mp3').play(0)
        draw_bg()
        gameover_img = pygame.image.load('resources/gameover.png')
        gameover_size = gameover_img.get_size()
        window.blit(gameover_img, ((window_width - gameover_size[0])/2, ((window_height - gameover_size[1])/2 - 50)))

        score_all = pygame.font.Font(font_source, 50).render(f'本次得分: {score_int}', True, (200, 62, 62))
        score_all_pos = score_all.get_size()
        score_ws = (window_width - score_all_pos[0]) / 2
        score_hs = (window_height - score_all_pos[1] + 75) / 2
        window.blit(score_all, (score_ws, score_hs))

        pygame.display.update()
        try:
            url2 = 'http://39.105.170.197:5000/submit'
            data2 = {'username': userinputs[0], 'score': score_int}
            r2 = requests.post(url2, data=data2)
            # 打印响应时间单位s
            r2_time = r2.elapsed.microseconds / 1000000
            # 打印响应结果
            r2_text = r2.text
            print(f'你的最终分数为：{r2_text} 用时：{r2_time}')
        except:
            pass
        pygame.time.wait(7500)
        pygame.quit()
        sys.exit()

    active_time += 1

    if active_time % speed == 0:
        if active == 1:  # 上
            rh -= 25
        if active == 2:  # 下
            rh += 25
        if active == 3:  # 左
            rw -= 25
        if active == 4:  # 右
            rw += 25

    pygame.draw.rect(window, (118, 37, 39), (rw, rh, 25, 25))  # 蛇
    # pygame.draw.rect(window, (1, 185, 237), (rwc, rhc, 25, 25))  # 糖果
    pygame.display.update()
    draw_bg()
    for rwhc_temp in rwhcs:
        pygame.draw.rect(window, (1, 185, 237), (rwhc_temp[0], rwhc_temp[1], 25, 25))
    pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            keys = event.key
            print(f'按下{keys}')
            if keys == 1073741906 or keys == 119:  # 上
                active = 1
            if keys == 1073741905 or keys == 115:  # 下
                active = 2
            if keys == 1073741904 or keys == 97:  # 左
                active = 3
            if keys == 1073741903 or keys == 100:  # 右
                active = 4

        if event.type == pygame.QUIT:
            try:
                url2 = 'http://39.105.170.197:5000/submit'
                data2 = {'username': userinputs[0], 'score': score_int}
                r2 = requests.post(url2, data=data2)
                # 打印响应时间单位s
                r2_time = r2.elapsed.microseconds / 1000000
                # 打印响应结果
                r2_text = r2.text
                print(f'你的最终分数为：{r2_text} 用时：{r2_time}')
            except:
                pass
            exit()
