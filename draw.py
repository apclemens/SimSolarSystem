#!/usr/bin/env python

# this takes data created by system.py and draws it into frames, which then
# gets turned into a gif

from os import listdir
from os.path import isfile, join
from progressbar import ProgressBar
import pickle,subprocess
from PIL import Image, ImageDraw, ImageFont

def main(n=1, deltat=""):
	
	toWrite = 'dt = '+deltat

	mypath = 'coordinates/'
	onlyfiles = [mypath+f for f in listdir(mypath) if isfile(join(mypath, f))]
	fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)

	histories = []
	for fName in onlyfiles:
		f = open(fName, 'r')
		l = ['fName']+f.read().split('\n')
		while '' in l:
			l.remove('')
		f.close()
		histories.append(l)

	rad = 2

	pbar = ProgressBar()
	memoryUse = pickle.load(open('memory.p','rb'))

	for i in pbar(range(1,len(histories[0]),int(1./n))):
		im = Image.new('RGBA', (1280, 720), (0, 255, 0, 0))
		draw = ImageDraw.Draw(im)
		draw.rectangle([(0,0),im.size], fill = (0,0,0) )
		draw.text((10,10), toWrite, font=fnt, fill=(255,255,255))
		for plan in histories:
			x = eval(plan[i].split(' ')[0].split(':')[1])*20+im.size[0]/2
			y = eval(plan[i].split(' ')[1].split(':')[1])*20+im.size[1]/2
			draw.ellipse((x-rad,y-rad,x+rad,y+rad), fill=(255,255,255))
		im.save('images/'+'%05d' % i +'.png')
	
	subprocess.check_output(('convert -delay 10 -loop 0 images/*.png gifs/'+deltat+'.gif').split(' '))

if __name__ == '__main__':
	main(1., '1d')
