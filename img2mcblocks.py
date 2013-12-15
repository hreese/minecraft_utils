#!/usr/bin/python

from PIL import Image
from colormath.color_objects import *
import re

re_sideonly = re.compile('_side|_front')
re_toponly = re.compile('_top')

def image2singlecolor(image):
	return image.resize( (1,1), resample=Image.ANTIALIAS).getpixel( (0,0) )

def loadtexture(filename):
	t = {}
	# keep image
	t['image'] = Image.open(filename).convert("RGB")
	# shrink image to obtain single
	color = image2singlecolor(t['image'])
	t['labcolor'] = RGBColor(*color, rgb_type='sRGB').convert_to('lab')
	# tag
	if re_sideonly.search(filename):
		t['tag_side'] = True
	elif re_toponly.search(filename):
		t['tag_top'] = True
	else:
		t['tag_side'] = True
		t['tag_top'] = True
	return t

# read image
i = Image.open('FastGhastBlast.png').convert("RGB")

# c1=RGBColor(188, 223, 214, rgb_type='sRGB').convert_to('lab')
# c1.delta_e(c3, mode='cmc', pl=1, pc=1)
# i.resize( (1,1), resample=Image.ANTIALIAS).getpixel( (0,0) )