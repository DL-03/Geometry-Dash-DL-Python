import pygame
import keyboard
import math
import sys
from tkinter import filedialog
from tkinter import *
import time
import json
from PIL import Image, ImageDraw

code = ''



player = {
	'x': 0,
	'y': 0,
	'vx': 11.75,
	'vy': -1
}

cam = {
	'x': 0,
	'y': 0,
	'vx': 0,
	'vy': 0
}

edit = {
	'mode': 0,
	'select': 'none'
}

main = 'main'
nameS = 0

# code = [{'name': 'Name Test'}, 'Music', [{'Object': 'Nblock1', 'x': 90, 'y': -45, 'size': 45}, {'Object': 'text', 'x': 135, 'y': -90, 'size': 45, 'caption': 'Hello!', 'color': (0, 0, 0)}, {'Object': 'Nblock1', 'x': 135, 'y': -45, 'size': 45}, {'Object': 'Nblock1', 'x': 270, 'y': -90, 'size': 45}]]

ColorP = ['#ffff00','#00c8ff']


toch = 1


def RGBtoHex(vals, rgbtype=1):
  if len(vals)!=3 and len(vals)!=4:
    raise Exception("RGB or RGBA inputs to RGBtoHex must have three or four elements!")
  if rgbtype!=1 and rgbtype!=256:
    raise Exception("rgbtype must be 1 or 256!")

  #Convert from 0-1 RGB/RGBA to 0-255 RGB/RGBA
  if rgbtype==1:
    vals = [255*x for x in vals]

  #Ensure values are rounded integers, convert to hex, and concatenate
  return '#' + ''.join(['{:02X}'.format(int(round(x))) for x in vals])



# initialize pygame
pygame.init()

# create display & run update
width = 1000
height = 700
fps = 60
display = pygame.display.set_mode((width, height))

pygame.display.update()
pygame.display.set_caption("Geometry Dash DL")
clock = pygame.time.Clock()
GameP = True

_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render(text, font, gfcolor, ocolor=(0, 0, 0), opx=2.5):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height() + 5

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf

def jsons(pui):
	global code
	global main
	global edit
	with open(pui, 'r') as file:
		put = json.load(file)
	code = put
	main = 'game'
	edit['Mode'] = 0

def editor():
	s = pygame.Surface((width,height-150), pygame.SRCALPHA)
	s.fill((0,0,0,128))                       
	display.blit(s, (0, height-150))
	cam['x'] = cam['vx']
	cam['y'] = cam['vy'] + height-300
	if keyboard.is_pressed('left arrow'):
		cam['vx'] += 10
	if keyboard.is_pressed('right arrow'):
		cam['vx'] -= 10
	if keyboard.is_pressed('up arrow'):
		cam['vy'] += 10
	if keyboard.is_pressed('down arrow'):
		cam['vy'] -= 10
	button('Block', width/2, height/1.2, 'PUSAB.otf', 24, (0, 0, 0), 'ED Nblock1')
	if nameS == 'ED Nblock1':
		edit['select'] = nameS[3:]
	button('Spike', width/2, height/1.2+45, 'PUSAB.otf', 24, (0, 0, 0), 'ED Nspike1')
	if nameS == 'ED Nspike1':
		edit['select'] = nameS[3:]
	# button('Text', width/2, height/1.2+90, 'PUSAB.otf', 24, (0, 0, 0), 'ED text')
	# if nameS == 'ED text':
	# 	edit['select'] = nameS[3:]
	if event.type == pygame.MOUSEBUTTONDOWN:
		code[2].append({'Object': edit['select'], 'x': -1*(cam['x']) + round(mouseP[0]/45)*45, 'y': -1*(cam['y']) + round(mouseP[1]/45)*45, 'size': 45})
rusts = 0
def peCColor(types, colorRGB, name, u):
			global rusts
			name = 'peC-' + name + str(types)
			button('', width/6 + (60*u), height/1.5 + (65*types), 'PUSAB.otf', 24, (255, 255, 255), name, sizes = [45, 45], colorB = [colorRGB, (0, 0, 0)], colorBS = [colorRGB, (200, 200, 0)])
			if nameS == name:
				if types == 0:
					ColorP[0] = RGBtoHex((colorRGB), rgbtype=256)
				else:
					ColorP[1] = RGBtoHex((colorRGB), rgbtype=256)
				PlayerIco()
			rusts += 1

def button(caption, x, y, font, fontSize, fontColor, name, colorB = [(0, 200, 0), (0, 150, 0)], colorBS = [(200, 200, 0), (150, 150, 0)], sizes = 0):
	global nameS
	global mouseP
	if sizes == 0:
		sizeex = 10 + (len(caption)*(fontSize))
		sizeey = (fontSize)+10
	else:
		sizeex = sizes[0]
		sizeey = sizes[1]
	
	if mouseP[0] > x - (sizeex/2) and mouseP[0] < x + (sizeex/2) and mouseP[1] > y - (sizeey/2) and mouseP[1] < y + (sizeey/2):
		pygame.draw.rect(display, colorBS[1], [
						x-(sizeex/2)-5,
						y-(sizeey/2)-5,
						sizeex+10,
						sizeey+10])
		pygame.draw.rect(display, colorBS[0], [
						x-(sizeex/2),
						y-(sizeey/2),
						sizeex,
						sizeey])
		if event.type == pygame.MOUSEBUTTONDOWN:
			nameS = name
			time.sleep(0.1)
		else:
			nameS = 0
	else:
		pygame.draw.rect(display, colorB[1], [
						x-(sizeex/2)-5,
						y-(sizeey/2)-5,
						sizeex+10,
						sizeey+10])
		pygame.draw.rect(display, colorB[0], [
						x-(sizeex/2),
						y-(sizeey/2),
						sizeex,
						sizeey])
	text(caption, x-(sizeex/4), y-(sizeey/4), font, fontSize, fontColor)
	

def text(caption, x, y, font, fontSize, fontColor):
    # font2 = pygame.font.Font(font, fontSize+5)
    # text2 = font2.render(caption, True, (0, 0, 0))
    # place2 = text2.get_rect(center=(x, y))
    # display.blit(text2, place2)
    # font1 = pygame.font.Font(font, fontSize)
    # text1 = font1.render(caption, True, (fontColor))
    # place1 = text1.get_rect(center=(x, y))
    # display.blit(text1, place1)
	fonts = pygame.font.Font(font, fontSize)
	display.blit(render(caption, fonts, gfcolor = fontColor), (x, y))

def Objects():
	global toch
	for i in range(0, len(code['Code'])):
		xs = code['Code'][i].get('x')
		xs2 = code['Code'][i].get('xo')
		ys = code['Code'][i].get('y')
		ys2 = code['Code'][i].get('yo')
		xs3 = 0
		ys3 = 0
		if xs != None:
			xs3 += xs
		if xs2 != None:
			xs3 += xs2*code['Code'][i]['size']
		if ys != None:
			ys3 += ys
		if ys2 != None:
			ys3 += ys2*code['Code'][i]['size']





		Temp = [code['Code'][i]['Object'], xs3, ys3, code['Code'][i]['size']]
		if Temp[0] == 'Nblock1':
			display.blit(Nblock1img, (cam['x'] + Temp[1], cam['y'] + Temp[2], Temp[3], Temp[3]))
			if player['y'] > Temp[2] - Temp[3] - Temp[3]/8 and player['y'] < Temp[2] + Temp[3]/2 and player['x'] < Temp[1] + Temp[3] - Temp[3]/6 - 1 and player['x'] > Temp[1] - Temp[3] + Temp[3]/6 + 1:
				if player['y'] > Temp[2] - Temp[3] and player['y'] < Temp[2] + Temp[3]/2 and player['x'] < Temp[1] + Temp[3] - Temp[3]/8 - 1 and player['x'] > Temp[1] - Temp[3] + Temp[3]/8 + 1:
					player['y'] = Temp[2] - Temp[3]
					player['vy'] = -1
					toch += 1
			else:
				if player['x'] < Temp[1] + Temp[3] + 1 and player['x'] > Temp[1] - Temp[3]/2 and player['y'] > Temp[2] - Temp[3] + Temp[3]/8 + 1 and player['y'] < Temp[2] + Temp[3] - Temp[3]/8 - 1:
					player['x'] = Temp[1] + Temp[3]
				if player['x'] < Temp[1] + Temp[3]/2 and player['x'] > Temp[1] - Temp[3] - 1 and player['y'] > Temp[2] - Temp[3] + Temp[3]/8 + 1 and player['y'] < Temp[2] + Temp[3] - Temp[3]/8 - 1:
					player['x'] = Temp[3]
				if player['y'] > Temp[2] - Temp[3]/2 and player['y'] < Temp[2] + Temp[3] - 1 and player['x'] < Temp[1] + Temp[3] - Temp[3]/8 - 1 and player['x'] > Temp[1] - Temp[3] + Temp[3]/8 + 1:
					player['y'] = Temp[2]
		if Temp[0] == 'Nspike1':
			# pygame.draw.rect(display, (0, 125, 255), [
			# 		cam['x'] + code[2][i]['x'],
			# 		cam['y'] + code[2][i]['y'],
			# 		code[2][i]['size'],
			# 		code[2][i]['size']])
			display.blit(Nspike1img, (cam['x'] + Temp[1], cam['y'] + Temp[2], Temp[3], Temp[3]))
			if player['x'] > Temp[1] - (Temp[3]/1.25) and player['x'] < Temp[1] + (Temp[3]/1.25) and player['y'] > Temp[2] - Temp[3] and player['y'] < Temp[2] + (Temp[3]/1.25):
				player['x'] = 0
		if Temp[0] == 'text':
			text(code['Code'][i]['caption'], cam['x'] + Temp[1], cam['y'] - Temp[1], 'PUSAB.otf', Temp[3], code['Code'][i]['color'])
			
Nblock1img = pygame.image.load('Resources\\Objects\\Nblock1.png').convert_alpha()
Nspike1img = pygame.image.load('Resources\\Objects\\Nspike1.png').convert_alpha()









Logo = pygame.image.load('Resources\\logo.png').convert_alpha()
lw = 1486/2
lh = 399/2
Logo = pygame.transform.scale(Logo, (round(lw), round(lh)))

BGimg = pygame.image.load('Resources\\BG.png').convert_alpha()
BGIimg = pygame.transform.flip(BGimg, True, False)
Fimg = pygame.image.load('Resources\\flor.png').convert_alpha()


cam['y'] = 500

def players():
	if player['y'] > (45*-5):
		cam['y'] = 500
	else:
		cam['y'] = -1*(player['y'] - (height-150))-150
	# cam['x'] = -1*(player['x'] - 200)
	# cam['x'] = -1*((player['x']) -200)
	cam['x'] -= (-1*((player['x'])-200) + cam['x'])/8 - (-1*((player['x'])-200)/4)
	cam['y'] -= (-1*(player['y'] - (height-150))-750 + cam['y'])/8 - ((-1*(player['y'] - (height-150))-750 + cam['y'])/4)
	global toch
	# pygame.draw.rect(display, (0, 255, 0), [
	# 		cam['x'] + player['x'],
	# 		cam['y'] + player['y'],
	# 		45,
	# 		45])
	Pico = (cam['x'] + player['x'], cam['y'] + player['y'], 45, 45)
	display.blit(Pimg, Pico)

	if keyboard.is_pressed('left arrow'):
		player['x'] -= player['vx']/(fps/30)
	if keyboard.is_pressed('right arrow'):
		player['x'] += player['vx']/(fps/30)
	player['y'] -= player['vy']
	if player['vy'] != 0:
			try:
				player['vy'] -= math.sqrt(player['vy']/(fps/30))
			except Exception:
				player['vy'] -= math.sqrt(-1*player['vy']/(fps/30))	
	if player['y'] > 1:
		player['y'] = 0
		player['vy'] = 0
	if player['y'] > -1:
		toch += 1
	if (keyboard.is_pressed('space') or keyboard.is_pressed('up arrow')) and toch != 0:
		player['y'] -= 1
		player['vy'] += 30

def games():
	Objects()
	if edit['mode'] == 1:
		editor()
	else:
		players()
	# if edit['mode'] == 1:
	# 	button('Play', 90, 45, 'PUSAB.otf', 24, (0, 0, 0), 'ED')
	# else:
	# 	button('Edit', 90, 45, 'PUSAB.otf', 24, (0, 0, 0), 'ED')
	# if nameS == 'ED':
	# 	if edit['mode'] == 1:
	# 		edit['mode'] = 0
	# 	else:
	# 		edit['mode'] = 1
def PlayerIco():
	global Pimg
	img = Image.open('Resources\\Players\\ico4.png')
	w = img.size[0]
	h = img.size[1]
	p = img.load()
	idraw = ImageDraw.Draw(img)
	for wi in range(w):
	    for hi in range(h):
	        a = p[wi, hi][0]
	        b = p[wi, hi][1]
	        c = p[wi, hi][2]
	        if a == 1 and b == 0 and c == 0:
	        	idraw.rectangle((wi, hi, wi, hi), fill = ColorP[0])
	        if a == 2 and b == 0 and c == 0:
	        	idraw.rectangle((wi, hi, wi, hi), fill = ColorP[1])

	mode = img.mode
	size = img.size
	data = img.tobytes()

	Pimg = pygame.image.fromstring(data, size, mode)
PlayerIco()

ListColorP = [1, 2]

while GameP:
	

	mouseP = pygame.mouse.get_pos()
	clock.tick(fps)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GameP = False
	display.fill((0,0,0))
	for x in range(-1, 4):
		BGico = (cam['x']/4 - 250 + (1000*x), cam['y']/2 - 500, 100, 100)
		if x%2 == 0:
			display.blit(BGimg, BGico)
		else:
			display.blit(BGIimg, BGico)
	
	for x in range(-1, 7):
		Fico = (cam['x'] - 250 + (1000*x), cam['y'] + 45, 100, 100)
		display.blit(Fimg, Fico)


	s = pygame.Surface((width,height), pygame.SRCALPHA)
	s.fill((0,0,255,125))                       
	display.blit(s, (0, 0))

	if main == 'pe':
		button('<', 45, 45, 'PUSAB.otf', 36, (255, 255, 255), 'BACKmain', sizes = [45, 45])
		if nameS == 'BACKmain':
			main = 'main'
		Pico = (width/2-22.5, height/4, 45, 45)
		display.blit(Pimg, Pico)

		

		button('<', width/6 - 70, height/1.5 + 65/2, 'PUSAB.otf', 36, (255, 255, 255), 'ColorP<', sizes = [45, 45])
		if nameS == "ColorP<":
			ListColorP[0] -= 1
			if ListColorP[0] < 1:
				ListColorP[0] = ListColorP[1]
		button('>', width - width/6 + 70, height/1.5 + 65/2, 'PUSAB.otf', 36, (255, 255, 255), 'ColorP>', sizes = [45, 45])
		if nameS == "ColorP>":
			ListColorP[0] += 1
			if ListColorP[0] > ListColorP[1]:
				ListColorP[0] = 1

		# pygame.draw.circle(display, [255, 255, 255, 125], 
	 #               (width/2-7.5/2, height/1.2), 7.5)
		def draw_circle_alpha(surface, color, center, radius):
		    target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
		    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
		    pygame.draw.circle(shape_surf, color, (radius, radius), radius)
		    surface.blit(shape_surf, target_rect)



		draw_circle_alpha(display, (255, 255, 255, 150), (width/2-7.5/2-10, height/1.2), 7.5)
		draw_circle_alpha(display, (255, 255, 255, 150), (width/2-7.5/2+10, height/1.2), 7.5)

		if ListColorP[0] == 1:
			draw_circle_alpha(display, (255, 255, 255, 255), (width/2-7.5/2-10, height/1.2), 7.5)
			for t in range(0, 2):
				rusts = 0
				peCColor(t, (127, 255, 3), 'green1', rusts)
				peCColor(t, (0, 255, 1), 'green2', rusts)
				peCColor(t, (0, 255, 125), 'green3', rusts)
				peCColor(t, (0, 255, 255), 'cyan1', rusts)
				peCColor(t, (0, 198, 255), 'cyan2', rusts)
				peCColor(t, (0, 125, 254), 'blue1', rusts)
				peCColor(t, (0, 0, 254), 'blue2', rusts)
				peCColor(t, (125, 0, 255), 'purple1', rusts)
				peCColor(t, (184, 0, 253), 'purple2', rusts)
				peCColor(t, (255, 0, 254), 'pink1', rusts)
				peCColor(t, (255, 1, 125), 'pink2', rusts)
				peCColor(t, (254, 0, 0), 'red1', rusts)
		if ListColorP[0] == 2:
			draw_circle_alpha(display, (255, 255, 255, 255), (width/2-7.5/2+10, height/1.2), 7.5)
			for t in range(0, 2):
				rusts = 0
				peCColor(t, (255, 76, 1), 'orange1', rusts)
				peCColor(t, (255, 125, 1), 'orange2', rusts)
				peCColor(t, (255, 185, 0), 'yellow1', rusts)
				peCColor(t, (255, 255, 0), 'yellow2', rusts)
				peCColor(t, (255, 255, 255), 'white1', rusts)
				peCColor(t, (174, 174, 174), 'gray1', rusts)
				peCColor(t, (89, 89, 89), 'gray2', rusts)
				peCColor(t, (0, 0, 0), 'black1', rusts)
				peCColor(t, (125, 123, 0), 'Ygreen1', rusts)
				peCColor(t, (101, 150, 0), 'Ygreen2', rusts)
				peCColor(t, (72, 175, 0), 'Ygreen3', rusts)
				peCColor(t, (0, 150, 0), 'green4', rusts)



	if main == 'game':
		games()
		button('<', 45, 45, 'PUSAB.otf', 36, (255, 255, 255), 'BACKmain', sizes = [45, 45])
		if nameS == 'BACKmain':
			main = 'main'
	
	if main == 'main':
		Logoico = (width/2-1486/4, height/4-399/4, 0, 0)
		display.blit(Logo, Logoico)
		button('Play', width/2, height/2+100, 'PUSAB.otf', 24, (255, 255, 255), 'play')
		if nameS == 'play':
			# main = 'Company'
			jsons("Level\\Company\\Stereo Madness.json")
		button('Import', width/2 + width/4, height/2+100, 'PUSAB.otf', 24, (255, 255, 255), 'edit')
		if nameS == 'edit':
			window = Tk()
			window.title("Loading")
			window.geometry('0x0')
			window.fileName = filedialog.askopenfilename(filetypes=(("Map Json", ".json"),   ("All Files", "*.*")))
			op = window.fileName
			jsons(op)
			window.destroy()
		button('Player', width/4, height/2+100, 'PUSAB.otf', 24, (255, 255, 255), 'pe')
		if nameS == 'pe':
			main = 'pe'

	
		
	text('v0.1', width/2-30, 24*1, 'PUSAB.otf', 24, (255, 255, 0))

	# text('Mouse X: ' + str(mouseP[0]), width/2, 24*3, 'PUSAB.otf', 24, (0, 0, 0))
	# text('Mouse Y: ' + str(mouseP[1]), width/2, 24*4, 'PUSAB.otf', 24, (0, 0, 0))
	# text('Mouse X 45: ' + str(-1*(cam['x']) + round(mouseP[0]/45)*45), width/2, 24*6, 'PUSAB.otf', 24, (0, 0, 0))
	# text('Mouse Y 45: ' + str(-1*(cam['y']) + round(mouseP[1]/45)*45), width/2, 24*7, 'PUSAB.otf', 24, (0, 0, 0))
	# text('Player X: ' + str(player['x']), width/2, 24*1, 'PUSAB.otf', 24, (0, 255, 0))
	# text('Player Y: ' + str(player['y']), width/2, 24*2, 'PUSAB.otf', 24, (0, 255, 0))
	# text('Player VX: ' + str(player['vx']), width/2, 24*3, 'PUSAB.otf', 24, (0, 255, 0))
	# text('Player VY: ' + str(player['vy']), width/2, 24*4, 'PUSAB.otf', 24, (0, 255, 0))

	# if main == 'Company':
	# 	s = pygame.Surface((width-(width/5)*2, 200), pygame.SRCALPHA)
	# 	s.fill((0,0,0,175))                       
	# 	display.blit(s, (width/5, height/4))
	# 	text('Stereo Madness', width/2-200, height/4+height/8, 'PUSAB.otf', 36, (255, 255, 255))

	

	pygame.display.update()
	toch = 0
	nameS = 0
pygame.quit()
quit()