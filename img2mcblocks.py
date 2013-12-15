#!/usr/bin/python

from PIL import Image
from colormath.color_objects import *
import re, os

re_sideonly = re.compile('_side|_front')
re_toponly = re.compile('_top')

class Texture:
	"""Minecraft texture"""
	def __init__(self):
		self.tags = {}

	def loadfile(self, filename):
		# keep image
		self.image = Image.open(filename).convert("RGB")

		# shrink image to obtain single
		self.singlecolor = self.image.resize( (1,1), resample=Image.ANTIALIAS).getpixel( (0,0) )

		# convert to Lab colorspace for better comparison
		self.rgbcolor = RGBColor(*self.singlecolor, rgb_type='sRGB')
		self.labcolor = self.rgbcolor.convert_to('lab')

		# tag
		if re_sideonly.search(filename):
			self.tags['side'] = True
		elif re_toponly.search(filename):
			self.tags['top'] = True
		else:
			self.tags['side'] = True
			self.tags['top'] = True
			self.tags['uniform'] = True

	def tags(self):
		return self.tags.keys()

	def singlecolor(self):
		return self.singlecolor

class TexturePack():
	"""Collection of textures"""
	def __init__(self):
		self.textures = {}

	def loaddir(self, dir = 'textures'):
		# load all images in dir
		for root, dirs, files in os.walk(dir):
			for f in files:
				filename = os.path.join(root,f)
				if os.path.isfile(filename):
					try:
						# load texture
						t = Texture()
						t.loadfile(filename)
						self.textures[filename] = t
					except IOError:
						pass

# read image
i = Image.open('FastGhastBlast.png').convert("RGB")

t = TexturePack()
t.loaddir('textures')

# c1=RGBColor(188, 223, 214, rgb_type='sRGB').convert_to('lab')
# c1.delta_e(c3, mode='cmc', pl=1, pc=1)
# i.resize( (1,1), resample=Image.ANTIALIAS).getpixel( (0,0) )
