import pygame
import keyboard
import math
import sys
from tkinter import filedialog
from tkinter import *
import time
import json
from PIL import Image, ImageDraw
import os



code = ''



player = {
	'x': 0,
	'y': 0,
	'vx': 5,
	'vy': -1,
	'mode': ''
}

cam = {
	'x': 0,
	'y': 0,
	'vx': 0,
	'vy': 0
}

edit = {
	'mode': 0,
	'select': 'none',
	'rule': False
}

main = 'main'
nameS = 0

op = ''

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

NameD = False





def text(caption, x, y, font, fontSize, fontColor):
	fonts = pygame.font.Font(font, fontSize)
	display.blit(render(caption, fonts, gfcolor = fontColor), (x, y))

def button(caption, x, y, font, fontSize, fontColor, name, colorB = [(0, 200, 0), (0, 150, 0)], colorBS = [(200, 200, 0), (150, 150, 0)], sizes = 0, ico = 'none', icons = 'none', inv = 0):
	global nameS
	global mouseP
	if sizes == 0:
		sizeex = 10 + (len(caption)*(fontSize))
		sizeey = (fontSize)+10
	else:
		sizeex = sizes[0]
		sizeey = sizes[1]
	
	if mouseP[0] > x - (sizeex/2) and mouseP[0] < x + (sizeex/2) and mouseP[1] > y - (sizeey/2) and mouseP[1] < y + (sizeey/2):
		if inv == 0:
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
		if inv == 0:
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
	if ico != 'none':
		icoI = pygame.image.load('Resources\\' + ico).convert_alpha()
		if sizes != 0:
			icoI = pygame.transform.scale(icoI, sizes)
		display.blit(icoI, (x-(sizeex/2), y-(sizeey/2), 0, 0))
	if icons != 'none':
		icoI = icons
		if sizes != 0:
			icoI = pygame.transform.scale(icoI, sizes)
		display.blit(icoI, (x-(sizeex/2), y-(sizeey/2), 0, 0))
	text(caption, x-(sizeex/4)-5, y-(sizeey/4), font, fontSize, fontColor)


def input(caption, x, y, font, fontSize, fontColor, name, colorB = [(150, 200, 150), (0, 150, 0)], colorBS = [(200, 200, 150), (150, 150, 0)], sizes = 0, texts = ''):
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
		# print(keyboard.hook())
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

	text(caption, x - (sizeex/2) + 5, y - (sizeex/y) - sizes[1]/4 + 2.5, font, fontSize, (150, 150, 150))


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

def render(text, font, gfcolor, ocolor=(0, 0, 0), opx=2.5, pos = ['left', 'center']):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() * opx
    h = font.get_height() * opx

    osurf = pygame.Surface((w, h)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    if pos[0] == 'left':
    	x = 0
    elif pos[0] == 'center':
    	x = w/2
    elif pos[0] == 'right':
    	x = w

    if pos[1] == 'up':
    	y = 0
    elif pos[1] == 'center':
    	y = h/2
    elif pos[1] == 'down':
    	y = h

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx + x, dy + opx))
    
    surf.blit(textsurface, (opx + x, opx))
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
	player['mode'] = code['Mode']

ends = 0 


ListObjectED = [1, 1]

ObjectWiew = [['Nblock1', 'Block'], ['Mblock1', 'Block'], ['Mblock2', 'Block'], ['Mblock3', 'Block'], ['Mblock4', 'Block'], ['Mblock5', 'Block'], ['Mblock6', 'Block'], ['Mblock7', 'Block'], ['Mblock8', 'Block'], ['NHalfblock1', 'Half Block'], ['Nspike1', 'Spike'], ['NHalfspike1', 'Half Spike'], ['Lspike1', 'Half Spike'], ['Pcube', 'Portal'], ['Pship', 'Portal']]

for g in range(0, len(ObjectWiew)):
	ObjectWiew[g].append(pygame.image.load('Resources\\Objects\\' + ObjectWiew[g][0] + '.png').convert_alpha()) 

Rot = 0
EDgrid = 1






class UI():
	def text( Position, Caption, Font = ['PUSAB.otf', 24, (255, 255, 255), 2.5], pos = ['left', 'center'] ):
		fonts = pygame.font.Font(Font[0], Font[1])
		display.blit(render(Caption, fonts, gfcolor = Font[2], opx = Font[3], pos = pos), Position)
	def button( Position, Size, Caption, Font = ['PUSAB.otf', 24, (255, 255, 255), 2.5], pos = ['left', 'center'], colorB = [(0, 200, 0), (0, 150, 0)], colorBS = [(200, 200, 0), (150, 150, 0)], inv = 0, ico = 'none', icons = 'none'):
		global NameD
		global mouseP
		if pos[0] == 'left':
			x = Position[0]	
		elif pos[0] == 'center':
			x = Position[0] - Size[0]/2
		elif pos[0] == 'right':
			x = Position[0] - Size[0]

		if pos[1] == 'up':
			y = Position[1]
		elif pos[1] == 'center':
			y = Position[1] - Size[1]/2
		elif pos[1] == 'down':
			y = Position[1] - Size[1]
			
		if mouseP[0] > x and mouseP[0] < x + Size[0] and mouseP[1] > y and mouseP[1] < y + Size[1]:
			pygame.draw.rect(display, colorBS[1], [
								x - 5,
								y - 5,
								Size[0] + 10,
								Size[1] + 10])
			
			pygame.draw.rect(display, colorBS[0], [
									x,
									y,
									Size[0],
									Size[1]])
			if event.type == pygame.MOUSEBUTTONDOWN:
				NameD = True
				time.sleep(0.1)
			else:
				NameD = False
		
		else:
			pygame.draw.rect(display, colorB[1], [
								x - 5,
								y - 5,
								Size[0] + 10,
								Size[1] + 10])

			pygame.draw.rect(display, colorB[0], [
									x,
									y,
									Size[0],
									Size[1]])




		if ico != 'none':
			icoI = pygame.image.load('Resources\\' + ico).convert_alpha()
			icoI = pygame.transform.scale(icoI, Size)
			display.blit(icoI, x, y, 0, 0)
		if icons != 'none':
			icoI = icons
			icoI = pygame.transform.scale(icoI, Size)
			display.blit(icoI, x, y, 0, 0)
		UI.text(Caption = Caption, Position = [x + Font[3], y + Size[1]/4 + Font[3]], pos = ['center', 'center'], Font = Font)
	def input( Position, Text, Size, Caption, Font = ['PUSAB.otf', 24, (255, 255, 255), 2.5], pos = ['left', 'center'], colorB = [(200, 250, 200), (0, 150, 0)], colorBS = [(250, 250, 200), (150, 150, 0)], inv = 0, ico = 'none', icons = 'none'):
		global NameD
		global mouseP
		if pos[0] == 'left':
			x = Position[0]	
		elif pos[0] == 'center':
			x = Position[0] - Size[0]/2
		elif pos[0] == 'right':
			x = Position[0] - Size[0]

		if pos[1] == 'up':
			y = Position[1]
		elif pos[1] == 'center':
			y = Position[1] - Size[1]/2
		elif pos[1] == 'down':
			y = Position[1] - Size[1]
			
		if mouseP[0] > x and mouseP[0] < x + Size[0] and mouseP[1] > y and mouseP[1] < y + Size[1]:
			pygame.draw.rect(display, colorBS[1], [
								x - 5,
								y - 5,
								Size[0] + 10,
								Size[1] + 10])
			
			pygame.draw.rect(display, colorBS[0], [
									x,
									y,
									Size[0],
									Size[1]])
			NameD = True

				
		
		else:
			NameD = False
			pygame.draw.rect(display, colorB[1], [
								x - 5,
								y - 5,
								Size[0] + 10,
								Size[1] + 10])

			pygame.draw.rect(display, colorB[0], [
									x,
									y,
									Size[0],
									Size[1]])




		if ico != 'none':
			icoI = pygame.image.load('Resources\\' + ico).convert_alpha()
			icoI = pygame.transform.scale(icoI, Size)
			display.blit(icoI, x, y, 0, 0)
		if icons != 'none':
			icoI = icons
			icoI = pygame.transform.scale(icoI, Size)
			display.blit(icoI, x, y, 0, 0)
		if Text == '':
			UI.text(Caption = Caption, Position = [x + Font[3]*2, y + Size[1]/4 + Font[3]], pos = ['left', 'center'], Font = ['PUSAB.otf', 24, (150, 150, 150), 2.5])

		UI.text(Caption = Text, Position = [x + Font[3]*2, y + Size[1]/4 + Font[3]], pos = ['left', 'center'], Font = Font)





def editor():
	global code
	global EDgrid
	global ends
	global Rot
	global ObjectWiew
	global mouseP
	global cam
	global op


	# UI.text(Caption = 'hi', Position = [width/2, height/2], pos = ['center', 'center'])
	
	

	if EDgrid == 1:
		for v in range(0, round(width/45)+round(cam['x']/-45)):
			if cam['x']+(v*45) > 0 and cam['x']+(v*45) < width:
				pygame.draw.line(display, (0, 0, 0), (cam['x']+(v*45), 0), (cam['x']+(v*45), height), 1)
		for v in range(0, round(height/45)+round(cam['y']/45)):
			if cam['y']+(v*-45) > 0 and cam['y']+(v*-45) < height:
				pygame.draw.line(display, (0, 0, 0), (0, cam['y']+(v*-45)), (width, cam['y']+(v*-45)), 1)
	if event.type == pygame.MOUSEBUTTONDOWN and edit['select'] != 'none' and round((mouseP[0]-cam['x']-22.5)/45) > -1 and -1*(round((mouseP[1]-cam['y']-22.5)/45)) > -1 and mouseP[1] < height-200 and mouseP[1] > 80:
		if edit['select'] != 'Del':
			code['Code'].append({'Object': edit['select'], 'xo': round((mouseP[0]-cam['x']-22.5)/45), 'yo': -1*(round((mouseP[1]-cam['y']-22.5)/45)), 'size': 45, 'rots': Rot})
		else:
			for s in range(0, len(code['Code'])):
				if code['Code'][s]['xo'] == round((mouseP[0]-cam['x']-22.5)/45) and code['Code'][s]['yo'] == -1*(round((mouseP[1]-cam['y']-22.5)/45)):
					code['Code'].pop(s)
					break
		time.sleep(0.1)
	s = pygame.Surface((width,height-200), pygame.SRCALPHA)
	s.fill((0,0,0,128))                       
	display.blit(s, (0, height-200))
	cam['x'] = cam['vx']
	cam['y'] = cam['vy'] + height-300
	yu = 1
	if keyboard.is_pressed('shift'):
		yu = 2
	if keyboard.is_pressed('left arrow') or keyboard.is_pressed('a'):
		cam['vx'] += 20 * yu
	if keyboard.is_pressed('right arrow') or keyboard.is_pressed('d'):
		cam['vx'] -= 20 * yu
	if keyboard.is_pressed('up arrow') or keyboard.is_pressed('w'):
		cam['vy'] += 20 * yu
	if keyboard.is_pressed('down arrow') or keyboard.is_pressed('s'):
		cam['vy'] -= 20 * yu


	button('<', 180, height-100, 'PUSAB.otf', 36, (255, 255, 255), 'backOb ED', sizes = [45, 45])
	if nameS == "backOb ED":
		ListObjectED[0] -= 1
		if ListObjectED[0] < 1:
			ListObjectED[0] = ListObjectED[1]

	button('>', width - 180, height-100, 'PUSAB.otf', 36, (255, 255, 255), 'nextOb ED', sizes = [45, 45])
	if nameS == "nextOb ED":
		ListObjectED[0] += 1
		if ListObjectED[0] > ListObjectED[1]:
			ListObjectED[0] = 1


	
	


	if ListObjectED[0] == 1:
		ly = 0
		for l in range(0, len(ObjectWiew)):
			if l > 8:
				ly = 75
				button('', width/4 - 10 + (65*(l-9)), height/1.25 + ly, 'PUSAB.otf', 24, (255, 255, 255), 'ED ' + ObjectWiew[l][0], sizes = [45, 45], icons = ObjectWiew[l][2])
			else:
				button('', width/4 - 10 + (65*l), height/1.25 + ly, 'PUSAB.otf', 24, (255, 255, 255), 'ED ' + ObjectWiew[l][0], sizes = [45, 45], icons = ObjectWiew[l][2])
			if nameS == 'ED ' + ObjectWiew[l][0]:
				edit['select'] = nameS[3:]


	





	if EDgrid == 0:
		button('Grid', 80, height-100+20, 'PUSAB.otf', 16, (255, 255, 255), 'ED Grid', colorB = [(250, 0, 0), (200, 0, 0)], colorBS = [(250, 0, 0), (0, 200, 0)], sizes = [105, 24])
		if nameS == 'ED Grid':
			EDgrid = 1
	else:
		button('Grid', 80, height-100+20, 'PUSAB.otf', 16, (255, 255, 255), 'ED Grid', colorB = [(0, 250, 0), (0, 200, 0)], colorBS = [(0, 250, 0), (200, 0, 0)], sizes = [105, 24])
		if nameS == 'ED Grid':
			EDgrid = 0
	button('Delete', 80, height-100-20, 'PUSAB.otf', 16, (255, 255, 255), 'ED Del', colorB = [(250, 0, 0), (200, 0, 0)])
	if nameS == 'ED Del':
		edit['select'] = nameS[3:]

	


	text(str(Rot), width - 80, height-100 - 30, 'PUSAB.otf', 24, (255, 255, 255))

	button('-90', width - 115, height-100 + 30, 'PUSAB.otf', 16, (255, 255, 255), 'ED Rot-', sizes = [45, 45])
	if nameS == 'ED Rot-':
		Rot -= 90
		if Rot < 0:
			Rot = 270
	button('+90', width - 45, height-100 + 30, 'PUSAB.otf', 16, (255, 255, 255), 'ED Rot+', sizes = [45, 45])
	if nameS == 'ED Rot+':
		Rot += 90
		if Rot > 360:
			Rot = 90






	button('Save', width/1.1 - 200, 45, 'PUSAB.otf', 24, (255, 255, 255), 'ED Save')
	if nameS == 'ED Save':
		try:
			with open(op, 'w') as outfile:
				json.dump(code, outfile)
		except Exception:
			window = Tk()
			window.title("Loading")
			window.geometry('0x0')
			window.fileName = filedialog.asksaveasfilename(
                defaultextension='.json', filetypes=[("json files", '*.json')],
                title="Choose filename")			
			opt = window.fileName
			try:
				with open(opt, 'w') as outfile:
					json.dump(code, outfile)
				op = opt
			except Exception:
				pass
			window.destroy()
	button('Save As', width/1.1 - 25, 45, 'PUSAB.otf', 24, (255, 255, 255), 'ED SaveAs')
	if nameS == 'ED SaveAs':
		window = Tk()
		window.title("Loading")
		window.geometry('0x0')
		window.fileName = filedialog.asksaveasfilename(
          	    defaultextension='.json', filetypes=[("json files", '*.json')],
          	    title="Choose filename")			
		opt = window.fileName
		try:
			with open(opt, 'w') as outfile:
				json.dump(code, outfile)
			op = opt
		except Exception:
			pass
		window.destroy()

	UI.input(Caption = 'Name LVL', Text = code['Name'], Position = [width/4.5, 45], pos = ['left', 'center'], Size = [180, 35])
	if NameD == True:
		keyb = r'0123456789abcdefghijklmnopqrstuvwxyz '
		for k in keyb:
			if keyboard.is_pressed(k):
				if keyboard.is_pressed('shift'):
					code['Name'] += k.upper()
				else:
					code['Name'] += k
				time.sleep(0.1)
		if keyboard.is_pressed('\b'):
			code['Name'] = code['Name'][:-1]
			time.sleep(0.1)
		
	# button('Text', width/2, height/1.2+90, 'PUSAB.otf', 24, (0, 0, 0), 'ED text')
	# if nameS == 'ED text':
	# 	edit['select'] = nameS[3:]
	
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


	
end = []

def de():
	global code
	global player
	global cam
	cam['x'] = 0
	cam['y'] = 0
	player['x'] = 0
	player['y'] = 0
	player['mode'] = code['Mode']

def HitBoxe(Object, Temp):
	global player
	global toch
	if Object == 'Block':
		if player['y'] > Temp[2] - Temp[3] - Temp[3]/8 and player['y'] < Temp[2] + Temp[3]/2 and player['x'] < Temp[1] + Temp[3] + Temp[3]/10 - 1 and player['x'] > Temp[1] - Temp[3] - Temp[3]/10 + 1:
			
			if player['y'] > Temp[2] - Temp[3] and player['y'] < Temp[2] + Temp[3]/2 and player['x'] < Temp[1] + Temp[3] - Temp[3]/10 - 1 and player['x'] > Temp[1] - Temp[3] + Temp[3]/10 + 1:
				player['y'] = Temp[2] - Temp[3]
				player['vy'] = -1
				toch += 1
				
		else:
			if player['x'] < Temp[1] + Temp[3] + 1 and player['x'] > Temp[1] - Temp[3]/2 and player['y'] > Temp[2] - Temp[3] + Temp[3]/8 + 1 and player['y'] < Temp[2] + Temp[3] - Temp[3]/8 - 1:
				player['x'] = Temp[1] + Temp[3]
				de()
			if player['x'] < Temp[1] + Temp[3]/2 and player['x'] > Temp[1] - Temp[3] - 1 and player['y'] > Temp[2] - Temp[3] + Temp[3]/8 + 1 and player['y'] < Temp[2] + Temp[3] - Temp[3]/8 - 1:
				player['x'] = Temp[1] - Temp[3]
				de()
			if player['y'] > Temp[2] - Temp[3]/2 and player['y'] < Temp[2] + Temp[3] - 1 and player['x'] < Temp[1] + Temp[3] - Temp[3]/8 - 1 and player['x'] > Temp[1] - Temp[3] + Temp[3]/8 + 1:
				player['y'] = Temp[2]
				de()
	if Object == 'Half Block':
		if player['y'] > Temp[2] - Temp[3] - Temp[3]/8 and player['y'] < Temp[2] + Temp[3]/3 and player['x'] < Temp[1] + Temp[3] + Temp[3]/10 - 1 and player['x'] > Temp[1] - Temp[3] - Temp[3]/10 + 1:
			
			if player['y'] > Temp[2] - Temp[3] and player['y'] < Temp[2] + Temp[3]/3 and player['x'] < Temp[1] + Temp[3] - Temp[3]/10 - 1 and player['x'] > Temp[1] - Temp[3] + Temp[3]/10 + 1:
				player['y'] = Temp[2] - Temp[3]
				player['vy'] = -1
				toch += 1
				
		else:
			if player['x'] < Temp[1] + Temp[3] + 1 and player['x'] > Temp[1] - Temp[3]/2 and player['y'] > Temp[2] - Temp[3] + Temp[3]/16 + 1 and player['y'] < Temp[2] + Temp[3] - Temp[3]/16 - 1:
				player['x'] = Temp[1] + Temp[3]
				de()
			if player['x'] < Temp[1] + Temp[3]/2 and player['x'] > Temp[1] - Temp[3] - 1 and player['y'] > Temp[2] - Temp[3] + Temp[3]/16 + 1 and player['y'] < Temp[2] + Temp[3] - Temp[3]/16 - 1:
				player['x'] = Temp[1] - Temp[3]
				de()
			if player['y'] > Temp[2] - Temp[3]/2 and player['y'] < Temp[2] + Temp[3]/2 - 1 and player['x'] < Temp[1] + Temp[3] - Temp[3]/8 - 1 and player['x'] > Temp[1] - Temp[3] + Temp[3]/8 + 1:
				player['y'] = Temp[2]
				de()
	if Object == 'Spike':
		if player['x'] > Temp[1] - (Temp[3]/1.25) and player['x'] < Temp[1] + (Temp[3]/1.25) and player['y'] > Temp[2] - (Temp[3]/1.25) and player['y'] < Temp[2] + (Temp[3]/1.25):
			de()
	if Object == 'Half Spike':
		if player['x'] > Temp[1] - (Temp[3]/1.25) and player['x'] < Temp[1] + (Temp[3]/1.25) and player['y'] > Temp[2] - (Temp[3]/2.25) and player['y'] < Temp[2] + (Temp[3]/1.25):
			player['x'] = 0
	if Object == 'Portal':
		if Temp[4] == 0 or Temp[4] == 180 or Temp[4] == 360:
			if player['x'] > Temp[1] - (Temp[3]/1.25) and player['x'] < Temp[1] + (Temp[3]/1.25) and player['y'] > Temp[2] - ((Temp[3]*2)/1.25) and player['y'] < Temp[2] + ((Temp[3]*3)/1.25):
				player['mode'] = Temp[0][1:]
		else:
			if player['x'] > Temp[1] - (Temp[3]*2/1.25) and player['x'] < Temp[1] + (Temp[3]*3/1.25) and player['y'] > Temp[2] - ((Temp[3])/1.25) and player['y'] < Temp[2] + ((Temp[3])/1.25):
				player['mode'] = Temp[0][1:]


def Objects():
	global ObjectWiew
	global ends
	global end
	global toch
	end = []
	if len(code['Code']) != 0:
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


			xf = 0
			yf = 0
			if code['Code'][i]['Object'] == 'Pcube' or code['Code'][i]['Object'] == 'Pship':
				xf = 0
				yf = -45
				if code['Code'][i]['rots'] == 90 or code['Code'][i]['rots'] == 270:
					xf = -45
					yf = 0



			Temp = [code['Code'][i]['Object'], xs3 + xf, ys3*-1 + yf, code['Code'][i]['size'], code['Code'][i]['rots']]
			for u in range(0, len(ObjectWiew)):
				if Temp[0] == ObjectWiew[u][0]:
					img = pygame.transform.rotate(ObjectWiew[u][2], code['Code'][i]['rots'])

					display.blit(img, (cam['x'] + Temp[1], cam['y'] + Temp[2], Temp[3], Temp[3]))
					HitBoxe(ObjectWiew[u][1], Temp)
			if Temp[0] == 'text':
				text(code['Code'][i]['caption'], cam['x'] + Temp[1], cam['y'] - Temp[1], 'PUSAB.otf', Temp[3], code['Code'][i]['color'])
			end.append(Temp[1])
		ends = max(end)
		ends += 45*10
		if edit['mode'] == 0:
			pygame.draw.rect(display, (0, 0, 0), [
							cam['x'] + ends,
							0,
							1000,
							height])
			text('END', cam['x'] + ends + 50, height/2, 'PUSAB.otf', 36, (255, 255, 255))











Logo = pygame.image.load('Resources\\logo.png').convert_alpha()
lw = 1486/2
lh = 399/2
Logo = pygame.transform.scale(Logo, (round(lw), round(lh)))

BGimg = pygame.image.load('Resources\\BG.png').convert_alpha()
BGIimg = pygame.transform.flip(BGimg, True, False)
Fimg = pygame.image.load('Resources\\flor.png').convert_alpha()
FAimg = pygame.image.load('Resources\\florAD.png').convert_alpha()


cam['y'] = 500
SPimg = 0
SPPimg = 0

def PlayerIco():
	global Pimg
	global SPimg
	global SPPimg
	img = Image.open('Resources\\Players\\cube\\ico4.png')
	w = img.size[0]
	h = img.size[1]
	p = img.load()
	idraw = ImageDraw.Draw(img)
	for wi in range(w):
		for hi in range(h):
			a = p[wi, hi][0]
			b = p[wi, hi][1]
			c = p[wi, hi][2]
			d = p[wi, hi][3]
			if d == 0:
				idraw.rectangle((wi, hi, wi, hi), fill = '#00000000')
			elif a == 1 and b == 0 and c == 0:
				idraw.rectangle((wi, hi, wi, hi), fill = ColorP[0])
			elif a == 2 and b == 0 and c == 0:
				idraw.rectangle((wi, hi, wi, hi), fill = ColorP[1])

	Pc = img 

	mode = img.mode
	size = img.size
	data = img.tobytes()

	Pimg = pygame.image.fromstring(data, size, mode)



	Pc.thumbnail((22, 22), Image.ANTIALIAS)

	mode = img.mode
	size = img.size
	data = img.tobytes()

	SPPimg = pygame.image.fromstring(data, size, mode)

	img = Image.open('Resources\\Players\\ship\\ico1.png')

	w = img.size[0]
	h = img.size[1]
	p = img.load()
	idraw = ImageDraw.Draw(img)
	for wi in range(w):
		for hi in range(h):
			a = p[wi, hi][0]
			b = p[wi, hi][1]
			c = p[wi, hi][2]
			d = p[wi, hi][3]
			if d == 0:
				idraw.rectangle((wi, hi, wi, hi), fill = '#00000000')
			elif a == 1 and b == 0 and c == 0:
				idraw.rectangle((wi, hi, wi, hi), fill = ColorP[0])
			elif a == 2 and b == 0 and c == 0:
				idraw.rectangle((wi, hi, wi, hi), fill = ColorP[1])


				

	img2 = Image.new('RGBA', (60, 45), "#00000000")
	img2.paste(Pc, (20, 5), mask = Pc)
	img2.paste(img, (0, 0), mask = img)
	

	mode = img2.mode
	size = img2.size
	data = img2.tobytes()

	SPimg = pygame.image.fromstring(data, size, mode)

	

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

roty = 0

def players():
	global roty
	global ends
	global SPimg
	global Pimg
	global toch

	if player['y'] > (45*-5) or player['mode'] == 'ship':
		cam['y'] = 500
	else:
		cam['y'] = -1*(player['y'] - (height-150))-150
	# cam['x'] = -1*(player['x'] - 200)
	# cam['x'] = -1*((player['x']) -200)
	if player['x'] > ends-45*10:
		cam['x'] = -1*(ends-45*17.5)
	else:
		cam['x'] -= (-1*((player['x'])-200) + cam['x'])/8 - (-1*((player['x'])-200)/4)
	cam['y'] -= (-1*(player['y'] - (height-150))-750 + cam['y'])/8 - ((-1*(player['y'] - (height-150))-750 + cam['y'])/4)
	
	# pygame.draw.rect(display, (0, 255, 0), [
	# 		cam['x'] + player['x'],
	# 		cam['y'] + player['y'],
	# 		45,
	# 		45])
	
	# if player['mode'] == 'cube':
	player['x'] += player['vx']*(60/FPS)
	# elif player['mode'] == 'cube platformer':
	# 	if keyboard.is_pressed('left arrow') or keyboard.is_pressed('a'):
	# 		player['x'] -= player['vx']/(fps/30)
	# 	if keyboard.is_pressed('right arrow') or keyboard.is_pressed('d'):
	# 		player['x'] += player['vx']/(fps/30)
	player['y'] -= player['vy']
	if player['y'] > 1:
		player['y'] = 0
		player['vy'] = 0

	if player['y'] > -1:
		toch += 1

	
	if player['mode'] == 'cube':
		
		if (keyboard.is_pressed('space') or keyboard.is_pressed('up arrow') or keyboard.is_pressed('w') or event.type == pygame.MOUSEBUTTONDOWN) and toch != 0:
			player['y'] -= 1
			player['vy'] += 30
		if player['vy'] != 0:
			roty -= 6
			try:
				player['vy'] -= math.sqrt(player['vy']/2*(60/FPS))
			except Exception:
				player['vy'] -= math.sqrt(-1*player['vy']/2*(60/FPS))	
		
		Pico = (cam['x'] + player['x'], cam['y'] + player['y'], 45, 45)
		

		display.blit(Pimg, Pico)

	if player['mode'] == 'ship':
		if (keyboard.is_pressed('space') or keyboard.is_pressed('up arrow') or keyboard.is_pressed('w') or event.type == pygame.MOUSEBUTTONDOWN):
			if toch != 0:
				player['y'] -= 2
			player['vy'] += 1
		else:
			player['vy'] -= 1
		if player['y'] < -1*(500 + 1):
			player['y'] = -500
			player['vy'] = 0

		# Pico = (cam['x'] + player['x'], cam['y'] + player['y'], 45, 45)
		# display.blit(SPPimg, Pico)

		Pico = (cam['x'] + player['x'], cam['y'] + player['y'], 45, 45)
		display.blit(SPimg, Pico)

	
	
	



def games():
	global main
	if player['x'] > ends:
		if edit['rule'] == True:
			edit['mode'] = 1
		else:
			main = 'main'
	Objects()
	if edit['mode'] == 1:
		editor()
	else:
		players()
	
	if edit['rule']:
		if edit['mode'] == 1:
			button('Play', 135, 45, 'PUSAB.otf', 24, (255, 255, 255), 'ED')
		else:
			button('Edit', 135, 45, 'PUSAB.otf', 24, (255, 255, 255), 'ED')
		if nameS == 'ED':
			if edit['mode'] == 1:
				player['x'] = 0
				player['y'] = 0
				player['vy'] = -1
				edit['mode'] = 0
				de()
			else:
				edit['mode'] = 1


PlayerIco()

ListColorP = [1, 2]
LvlPage = 1


mainB = []
mainB.append(pygame.image.load("Resources\\main\\Play.png").convert_alpha())
mainB.append(pygame.image.load("Resources\\main\\Skins.png").convert_alpha())
mainB.append(pygame.image.load("Resources\\main\\More.png").convert_alpha())

ComB = []
ComB.append(pygame.image.load("Resources\\Company\\BG-Com-LVL.png").convert_alpha())
ComB.append(pygame.image.load("Resources\\IcoH\\easy.png").convert_alpha())
ComB.append(pygame.image.load("Resources\\ico\\star.png").convert_alpha())


FPS = fps

while GameP:
	start_time = time.time()
		

	mouseP = pygame.mouse.get_pos()
	clock.tick(fps)
	


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			GameP = False
	display.fill((0,0,0))
	for x in range(-1, 7):
		BGico = (cam['x']/4 - 250 + (1000*x), cam['y']/2 - 500, 100, 100)
		if x%2 == 0:
			display.blit(BGimg, BGico)
		else:
			display.blit(BGIimg, BGico)
	
	for x in range(-1, 15):
		Fico = (cam['x'] - 250 + (1000*x), cam['y'] + 45, 100, 100)
		display.blit(Fimg, Fico)

	

	s = pygame.Surface((width,height), pygame.SRCALPHA)
	s.fill((0,0,255,125))                       
	display.blit(s, (0, 0))

	FAico = (width/2-400, cam['y'] + 44, 0, 0)
	display.blit(FAimg, FAico)

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
			if edit['rule'] == True:
				try:
					with open(op, 'w') as outfile:
						json.dump(code, outfile)
				except Exception:
					window = Tk()
					window.title("Loading")
					window.geometry('0x0')
					window.fileName = filedialog.asksaveasfilename(
		                defaultextension='.json', filetypes=[("json files", '*.json')],
		                title="Choose filename")			
					opt = window.fileName
					try:
						with open(opt, 'w') as outfile:
							json.dump(code, outfile)
						op = opt
					except Exception:
						pass
					window.destroy()

	if main == 'more':
		button('<', 45, 45, 'PUSAB.otf', 36, (255, 255, 255), 'BACKmain', sizes = [45, 45])
		if nameS == 'BACKmain':
			main = 'main'

		button('Create', width/2, height/2, 'PUSAB.otf', 24, (255, 255, 255), 'createED')
		if nameS == 'createED':
				code = {
				 "Name": "",
				 "Star": 1, 
				 "Difficulty": "easy",
				 "Music": "none", 
				 "Mode": "cube", 
				 "Code": []
				}
				
				edit['rule'] = True
				edit['mode'] = 1
				player['x'] = 0
				player['y'] = 0
				player['vy'] = -1
				main = 'game'
				put = ''
				de()


		button('Open', width/2, height/2+65, 'PUSAB.otf', 24, (255, 255, 255), 'OpenED')
		if nameS == 'OpenED':
			window = Tk()
			window.title("Loading")
			window.geometry('0x0')
			window.fileName = filedialog.askopenfilename(filetypes=(("Map Json", ".json"),   ("All Files", "*.*")))
			op = window.fileName
			try:
				jsons(op)
				window.destroy()
				edit['rule'] = True
				edit['mode'] = 1
				player['x'] = 0
				player['y'] = 0
				player['vy'] = -1
				de()
			except Exception:
				window.destroy()

	if main == 'Company':

		button('<', 45, 45, 'PUSAB.otf', 36, (255, 255, 255), 'BACKmain', sizes = [45, 45])
		if nameS == 'BACKmain':
			main = 'main'
		lvls = os.listdir('Level\\Company\\')

		button('<', 75, height/2, 'PUSAB.otf', 36, (255, 255, 255), 'backCLVL', sizes = [45, 45])
		if nameS == 'backCLVL':
			LvlPage -= 1
			if LvlPage < 1:
				LvlPage = len(lvls)
		button('>', width-75, height/2, 'PUSAB.otf', 36, (255, 255, 255), 'nextCLVL', sizes = [45, 45])
		if nameS == 'nextCLVL':
			LvlPage += 1
			if LvlPage > len(lvls):
				LvlPage = 1



		button('', width - width/2, height/2, 'PUSAB.otf', 24, (255, 255, 255), 'PlayLVL', sizes = [764, 212], icons = ComB[0], inv = 1)
		if nameS == 'PlayLVL':
			jsons("Level\\Company\\" + lvls[LvlPage-1])
			edit['rule'] = False
			edit['mode'] = 0
			player['x'] = 0
			player['y'] = 0
			player['vy'] = -1
			de()


		button('', width/5, height/2, 'PUSAB.otf', 24, (255, 255, 255), '', sizes = [75, 75], icons = ComB[1], inv = 1)
		button('', width - width/6.8, height/2.55, 'PUSAB.otf', 24, (255, 255, 255), '', sizes = [50, 50], icons = ComB[2], inv = 1)
		text('1', width - width/5, height/2.65, 'PUSAB.otf', 36, (255, 255, 0))
		text(lvls[LvlPage-1][:-5], width/2-200, height/4+height/4.5, 'PUSAB.otf', 48, (255, 255, 255))

	
	if main == 'main':
		
		Logoico = (width/2-1486/4, height/4-399/4, 0, 0)
		display.blit(Logo, Logoico)
		button('', width/2-5, height/2+100, 'PUSAB.otf', 24, (255, 255, 255), 'play', sizes = [150, 150], icons = mainB[0], inv = 1)
		if nameS == 'play':
			main = 'Company'
			
		button('', width - width/3.25, height/2+100, 'PUSAB.otf', 24, (255, 255, 255), 'mores', sizes = [125, 125], icons = mainB[2], inv = 1)
		if nameS == 'mores':
			main = 'more'
			
		button('', width/3.25, height/2+100, 'PUSAB.otf', 24, (255, 255, 255), 'pe', sizes = [125, 125], icons = mainB[1], inv = 1)
		if nameS == 'pe':
			main = 'pe'
		button('Import', width/2, height/1.2, 'PUSAB.otf', 24, (255, 255, 255), 'import')
		if nameS == 'import':
			window = Tk()
			window.title("Loading")
			window.geometry('0x0')
			window.fileName = filedialog.askopenfilename(filetypes=(("Map Json", ".json"),   ("All Files", "*.*")))
			op = window.fileName
			try:
				jsons(op)
				window.destroy()
				edit['rule'] = False
				edit['mode'] = 0
				player['x'] = 0
				player['y'] = 0
				player['vy'] = -1
				de()
			except Exception:
				window.destroy()
		text('By: DL', 20, height - 45, 'PUSAB.otf', 24, (0, 200, 0))

	
		
	# text('v0.4', width/2-30, 24*1, 'PUSAB.otf', 24, (255, 255, 0))
	if round(1.0 / (time.time() - start_time)) < 16:
		p = (255, 0, 0)
	elif round(1.0 / (time.time() - start_time)) < 31:
		p = (255, 255, 0)
	else:
		p = (0, 255, 0)
	text(str(round(FPS)), width/2-30, 24*1.25, 'PUSAB.otf', 32, p)

	
	# text('Mouse X: ' + str(mouseP[0]), width/2, 24*3, 'PUSAB.otf', 24, (0, 0, 0))
	# text('Mouse Y: ' + str(mouseP[1]), width/2, 24*4, 'PUSAB.otf', 24, (0, 0, 0))
	# text('Mouse X 45: ' + str(-1*(cam['x']) + round(mouseP[0]/45)*45), width/2, 24*6, 'PUSAB.otf', 24, (0, 0, 0))
	# text('Mouse Y 45: ' + str(-1*(cam['y']) + round(mouseP[1]/45)*45), width/2, 24*7, 'PUSAB.otf', 24, (0, 0, 0))
	# text('Player X: ' + str(player['x']), width/2, 24*1, 'PUSAB.otf', 24, (0, 255, 0))
	# text('Player Y: ' + str(player['y']), width/2, 24*2, 'PUSAB.otf', 24, (0, 255, 0))
	# text('Player VX: ' + str(player['vx']), width/2, 24*3, 'PUSAB.otf', 24, (0, 255, 0))
	# text('Toch: ' + str(toch), width/2, 24*4, 'PUSAB.otf', 24, (0, 255, 0))

	

	if main != 'game':
		cam['x'] -= 11.75*(60/FPS)
		cam['y'] = 480+45
		if cam['x'] < -(599*11.75):
			cam['x'] = 0
	
	FPS = 1 / (time.time() - start_time)
	pygame.display.update()
	toch = 0
	nameS = 0
	NameD = False
pygame.quit()
quit()