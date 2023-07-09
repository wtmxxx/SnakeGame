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
