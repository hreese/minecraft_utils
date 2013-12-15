#!/usr/bin/python

from PIL import Image
from colormath.color_objects import *
import re, os

re_sideonly = re.compile('_side|_front')
re_toponly = re.compile('_top')

def image2singlecolor(image):
	return image.resize( (1,1), resample=Image.ANTIALIAS).getpixel( (0,0) )

def loadtexture(filename):
	t = { 'tags' : {} }
	# keep image
	t['image'] = Image.open(filename).convert("RGB")
	# shrink image to obtain single
	color = image2singlecolor(t['image'])
	# convert to Lab colorspace for better comparison
	t['labcolor'] = RGBColor(*color, rgb_type='sRGB').convert_to('lab')
	# tag
	if re_sideonly.search(filename):
		t['tags']['side'] = True
	elif re_toponly.search(filename):
		t['tags']['top'] = True
	else:
		t['tags']['side'] = True
		t['tags']['top'] = True
		t['tags']['uniform'] = True
	return t

def loadtextures(dir = 'textures'):
	textures = {}
	# load all imagaes in dir
	for root, dirs, files in os.walk(dir):
		for f in files:
			filename = os.path.join(root,f)
			if os.path.isfile(filename):
				try:
					# load texture
					t = loadtexture(filename)
					textures[filename] = t
				except IOError:
					pass
	return textures

# read image
i = Image.open('FastGhastBlast.png').convert("RGB")

t = loadtextures('textures')

# c1=RGBColor(188, 223, 214, rgb_type='sRGB').convert_to('lab')
# c1.delta_e(c3, mode='cmc', pl=1, pc=1)
# i.resize( (1,1), resample=Image.ANTIALIAS).getpixel( (0,0) )
