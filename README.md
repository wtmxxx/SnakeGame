# SnakeGame
一个Python & Pygame开发的贪吃蛇小游戏

由[Wotemo](https://www.wotemo.com/)自主编写

### 共有单机版，联机版和最新一步到位联机版三种

* #### **单机版不能保存得分**

* #### **联机版可以保存得分**

* #### **最新一步到位联机版可以保存得分**

### 注：
* #### 最新一步到位联机版使用的是[Leancould](https://leancloud.app/)读写数据
  #### 不懂Leancould的可以去百度一下
* #### 联机版需要flask框架

本文件夹中的SnakeUsers已安装好虚拟环境和Flask

------

### Flask基本安装方法：
**（联机版看，大神无视)**

1. 打开powershall
2. cd到SnakeUsers文件夹 cd C:\SnakeUsers
3. 构建虚拟环境 py -3 -m venv venv
4. 激活虚拟环境 venv\Scripts\activate
5. 安装Flask pip install Flask
6. 导出 `FLASK_APP` 环境变量 $env:FLASK_APP = "main.py"
7. 运行服务器 flask run --host=0.0.0.0

![进程展示--游戏结束](https://img.wotemo.com/img/snakegame_over.png)

### 下面展示最新一步到位联机版的Python代码
**（三个完整版代码可以在[Github](https://github.com/wtmxxx/SnakeGame)中找到)**

#### 第一部分：main.py
### 这个部分是程序的主代码，
```python
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
print('本代码由沃特陌(Wotemo)编写，未经授权，严禁转载')
print(' _      ______  ____________  _______')
print('| | /| / / __ \/_  __/ __/  |/  / __ \\')
print('| |/ |/ / /_/ / / / / _// /|_/ / /_/ /')
print('|__/|__/\____/ /_/ /___/_/  /_/\____/')
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
# 替换为您的appid和appkey
appid = 'bf0o5ie2uZLSWGcDEuneCFEB-MdYXbMMI'
appkey = 'XIch9T9F9YYtlJBvQkBTYO2A'
def create_user(username):
    headers = {
        'X-LC-Id': appid,
        'X-LC-Key': appkey,
        'Content-Type': 'application/json'
    }

    # 构建API请求URL
    url = 'https://snakegame.wotemo.com/1.1/classes/Snakegame'

    # 构建请求体
    data = {
        'user': username
    }

    # 发送POST请求
    response = requests.post(url, headers=headers, json=data)

    # 处理响应数据
    if response.status_code == 201:
        print(f"用户名'{username}'创建成功")
    else:
        print(f"未能创建用户名'{username}'")

def get_score(username):
    headers = {
        'X-LC-Id': appid,
        'X-LC-Key': appkey
    }
    # 构建API请求URL
    url = f'https://snakegame.wotemo.com/1.1/classes/Snakegame?where={{"user":"{username}"}}&keys=score'

    # 发送GET请求
    response = requests.get(url, headers=headers)

    # 处理响应数据
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            score = data['results'][0]['score']
            print(f"用户名为'{username}'的分数为: {score}")
            return score
        else:
            create_user(userinputs[0])
            print(f"用户名'{username}'无对应分数")
            return 0
    else:
        print("未能获取分数")

def update_score(username,new_score):
    headers = {
        'X-LC-Id': appid,
        'X-LC-Key': appkey,
        'Content-Type': 'application/json'
    }

    # 构建API请求URL
    url = f'https://snakegame.wotemo.com/1.1/classes/Snakegame?where={{"user":"{username}"}}'

    # 发送GET请求，获取用户记录的objectId
    response = requests.get(url, headers=headers)
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        object_id = data['results'][0]['objectId']

        # 构建更新请求URL
        update_url = f'https://snakegame.wotemo.com/1.1/classes/Snakegame/{object_id}'

        # 构建请求体
        data = {
            'score': new_score
        }

        # 发送PUT请求，更新分数值
        update_response = requests.put(update_url, headers=headers, json=data)

        # 处理响应数据
        if update_response.status_code == 200:
            print(f"用户名为 '{username}'的分数更新成功！！！")
        else:
            print(f"未能更新用户名为'{username}'的分数！")
    else:
        print(f"用户名'{username}'未创建")

try:
    score_int = get_score(userinputs[0])
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
speed = 475
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
            speed = 425
        if 500 <= score_int < 1000:
            score_int += 100
            speed = 400
            if len(rwhcs) <= 3:
                creat_candy(1)
        if 1000 <= score_int < 1500:
            score_int += 150
            speed = 350
            if len(rwhcs) <= 4:
                creat_candy(1)
        if 1500 <= score_int < 2000:
            score_int += 200
            speed = 325
            if len(rwhcs) <= 5:
                creat_candy(1)
        if 2000 <= score_int < 2500:
            score_int += 250
            speed = 300
            if len(rwhcs) <= 6:
                creat_candy(1)
        if 2500 <= score_int < 3000:
            score_int += 300
            speed = 275
            if len(rwhcs) <= 7:
                creat_candy(1)
        if 3000 <= score_int:
            score_int += 350
            speed = 250
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
            update_score(userinputs[0],score_int)
            print(f'你的最终分数为：{score_int}')
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
                update_score(userinputs[0], score_int)
                print(f'你的最终分数为：{score_int}')
            except:
                pass
            exit()
```

#### 第二部分：InputBox.py
### 这个部分是用来显示输入框的(用户登录输入)，这里在Tai-Hsuan Ho编写的基础上进行了修改
```python
# Written by Tai-Hsuan Ho
# Created on 2016/11/25, and developed on Python 3.4
#
# Call: InputBox(rect, **args) to create a input bar editor in region defined by rect.
#
# Keyword arguments include:
# font: font of the input text.
# text: text initially in the input bar when it is created.
# bk_image: background image of the text input bar.
# bk_color: background color of the text input bar, ignored when bk_image is specified.
# bd_color: border color, no border if this keyword is missing or None.
# text_color: color of the input text. White color if this keyword is missing.
#
# Return value:
# Return (input text, flag), where flag can be True, False, or None when pressing ENTER, 
# ESC, or receiving QUIT event.
#
# Comments: 
# The input bar is transparent if both bk_image and bk_color are not specified or None.
# There is a game loop inside this function, and all events will be ignore except for 
# the key events and QUIT, which will be put back to the event queue and exit the game 
# loop. 
#


import pygame
from pygame.locals import *

COLOR_WHITE 	= (255, 255, 255)

TEXT_MARGIN = 16
FPS = 20

ALPHABETS = 'abcdefghijklmnopqrstuvwxyz'
OTHER_KEYS = '`1234567890-=[]\;\',./'
SHIFT_KEYS  = '~!@#$%^&*()_+{}|:"<>?'
PRINTABLE = ' ' + ALPHABETS + OTHER_KEYS + SHIFT_KEYS

def _caps_lock(ch):
	# Convert the input char when Caps Lock is turned on.
	if ch in ALPHABETS:
		return chr(ord(ch) - ord('a') + ord('A'))
	else:
		return ch

def _shift_hold(ch, caps_lock):
	# Convert the input char when SHIFT key is hold.
	if ch in OTHER_KEYS:
		return SHIFT_KEYS[OTHER_KEYS.index(ch)]
	elif ch in ALPHABETS and not caps_lock:
		return chr(ord(ch) - ord('a') + ord('A'))
	else:
		return ch

def _draw_box(surface, bk_image, bk_color, display_backup, bd_color):
	# Draw background image or fill color to the base surface, and draw the border.
	(width, height) = surface.get_size()
	if bk_image:
		surface.blit(bk_image, (0, 0))
	elif bk_color:
		surface.fill(bk_color)
	else:
		surface.blit(display_backup, (0, 0))
	if bd_color:
		pygame.draw.rect(surface, bd_color, surface.get_rect(), 1)

def _draw_text(surface, input_chars, font, color, start_index, cursor_index, show_cursor):
	# Draw the input text, making sure the char at cursor index is shown on the screen.
	x = 0
	pos = [x]
	for i in range(len(input_chars)):
		x += font.size(input_chars[i])[0]
		pos.append(x)
	# Find the start index, so that the cursor can be seen in the input editor.
	if start_index >= cursor_index:
		start_index = max(0, cursor_index - 5)
	while pos[cursor_index] - pos[start_index] > (surface.get_width() - 2 * TEXT_MARGIN):
		start_index += 1
	# Draw text in the editor.
	h = font.size('a')[1]
	y = (surface.get_height() - h) // 2
	for i in range(start_index, len(input_chars)):
		img = font.render(input_chars[i], True, color)
		x = TEXT_MARGIN + pos[i] - pos[start_index]
		surface.blit(img, (x, y))
		if x + img.get_width() + TEXT_MARGIN > surface.get_width():
			break
	# Draw cursor and return the start index.
	if show_cursor:
		x = TEXT_MARGIN + pos[cursor_index] - pos[start_index]
		pygame.draw.line(surface, color, (x, y), (x, y + h))
	return start_index

def InputBox(rect, **args):
	# Draw a box for text input. Return (text, True) when ENTER is pressed, (text, False) when ESC pressed, and (text, None) when QUIT
	# event is received. When both bk_image and bk_color are not specified, the input editor is transparent.
	try: 	font = args['font']
	except: font = pygame.font.Font(None, 32)
	try: 	input_chars = list(args['text'])
	except: input_chars = []
	try: 	bk_image = args['bk_image']
	except: bk_image = None
	try:	bd_color = args['bd_color']
	except:	bd_color = None
	try:	bk_color = args['bk_color']
	except:	bk_color = None
	try:	text_color = args['text_color']
	except:	text_color = COLOR_WHITE
	# Set repeat key event.
	pygame.key.set_repeat(500, 50)
	# Get display background in region of the input box.
	display = pygame.display.get_surface()
	display_backup = display.subsurface(rect).copy()
	# Create surface.
	surface = pygame.Surface(rect.size)
	# Get input event and update the input box.
	n = 0
	start_index = 0
	cursor_index = len(input_chars)
	bNeedUpdate = True
	myClock = pygame.time.Clock()
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				display.blit(display_backup, rect)
				pygame.display.update(rect)
				pygame.event.post(pygame.event.Event(QUIT, {}))
				return (''.join(input_chars), None)
			# For key up event, check if enter or escape keys are pressed.
			elif event.type == KEYUP:
				if event.key in (K_ESCAPE, K_RETURN):
					display.blit(display_backup, rect)
					pygame.display.update(rect)
					return (''.join(input_chars), event.key is K_RETURN)
			# For key down event, process backspace, delete, left, right, home, end, and normal key inputs.
			elif event.type == KEYDOWN:
				bNeedUpdate = True
				# Backspace key, deleting the previous char and moving the cursor left.
				if event.key == K_BACKSPACE:
					if cursor_index >= 1:
						del input_chars[cursor_index - 1]
						cursor_index -= 1
				# Delete key, deleting the current char.
				elif event.key == K_DELETE:
					if cursor_index < len(input_chars):
						del input_chars[cursor_index]
				# Left arrow key, moving cursor index to the previous char.
				elif event.key == K_LEFT:
					if cursor_index >= 1:
						cursor_index -= 1
				# Right arrow key, moving cursor index to the next char.
				elif event.key == K_RIGHT:
					if cursor_index < len(input_chars):
						cursor_index += 1
				# HOME key, moving cursor index to start of the input chars.
				elif event.key == K_HOME:
					cursor_index = 0
				# END key, moving cursor index to end of the input chars.
				elif event.key == K_END:
					cursor_index = len(input_chars)
				# Otherwise, add printable key to the input char list.
				else:
					try:
						ch = chr(event.key)
						if ch in PRINTABLE:
							shift_hold = (event.mod & KMOD_SHIFT)
							caps_lock = (event.mod & KMOD_CAPS)
							if shift_hold:
								ch = _shift_hold(ch, caps_lock)
							elif caps_lock:
								ch = _caps_lock(ch)
							input_chars.insert(cursor_index, ch)
							cursor_index += 1
					except:
						pass
		# Update the display for every 0.5 second or when key down event is received.
		if bNeedUpdate or (n == 0) or (n == FPS // 2):
			_draw_box(surface, bk_image, bk_color, display_backup, bd_color)
			show_cursor = bNeedUpdate or (n == 0)
			start_index = _draw_text(surface, input_chars, font, text_color, start_index, cursor_index, show_cursor)
			display.blit(surface, rect)
			pygame.display.update(rect)
			bNeedUpdate = False
		n = (n + 1) % FPS
		myClock.tick(FPS)

# Test codes.
def main():
	rect = pygame.Rect(200, 250, 200, 40)
	name_input = InputBox(rect, text = '', bd_color = (66, 133, 244), bk_color = (229, 231, 206), text_color = (0, 0, 0))
	print(f'你好：{name_input}')
	return name_input
