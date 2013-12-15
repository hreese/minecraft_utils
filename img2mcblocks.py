#!/usr/bin/python

from PIL import Image
from colormath.color_objects import *
import re

re_sideonly = re.compile('_side|_front')
re_toponly = re.compile('_top')

# http://www.cse.unr.edu/~quiroz/inc/colortransforms.py
def rgb2lab ( inputColor ) :

	num = 0
	RGB = [0, 0, 0]

	for value in inputColor :
		 value = float(value) / 255

		 if value > 0.04045 :
			  value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
		 else :
			  value = value / 12.92

		 RGB[num] = value * 100
		 num = num + 1

	XYZ = [0, 0, 0,]

	X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
	Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
	Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
	XYZ[ 0 ] = round( X, 4 )
	XYZ[ 1 ] = round( Y, 4 )
	XYZ[ 2 ] = round( Z, 4 )

	XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047			# ref_X =  95.047	Observer=2deg, Illuminant= D65
	XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0			 # ref_Y = 100.000
	XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883		  # ref_Z = 108.883

	num = 0
	for value in XYZ :

		 if value > 0.008856 :
			  value = value ** ( 1/3 )
		 else :
			  value = ( 7.787 * value ) + ( 16 / 116 )

		 XYZ[num] = value
		 num = num + 1

	Lab = [0, 0, 0]

	L = ( 116 * XYZ[ 1 ] ) - 16
	a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
	b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )

	Lab [ 0 ] = round( L, 4 )
	Lab [ 1 ] = round( a, 4 )
	Lab [ 2 ] = round( b, 4 )

	return Lab

def rgba2lab ( color ):
	return rgb2lab (inputColor[:3])

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