#!/usr/bin/python

from PIL import Image
from colormath.color_objects import *
import re, os
from collections import OrderedDict

re_sideonly = re.compile('_side|_front')
re_toponly = re.compile('_top')

class Texture:
	"""Minecraft texture"""
	def __init__(self):
		self.tags = {}

	def loadfile(self, filename):
		# keep filename
		self.filename = filename

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

	def __str__(self):
		return self.filename

class TexturePack():
	"""Collection of textures"""
	def __init__(self):
		self.textures = {}
		self.match_cache = {}

	def loaddir(self, dir = 'textures'):
		"""Add all images in dir to the texture pack"""
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

	def getMatches(self, color):
		"""Return textures sorted by distance"""
		assert not isinstance(color, basestring), "color is not an RGB tuple"
		if self.match_cache.has_key(color):
			return self.match_cache.has_key(color)
		else:
			matches = {}
			labcolor = RGBColor(*color, rgb_type='sRGB').convert_to('lab')
			for t in self.textures.values():
				matches[t] = t.labcolor.delta_e(labcolor)
			self.match_cache[color] = matches
			#return OrderedDict(sorted(matches.items(), key=lambda t: t[1]))
			return matches

t = TexturePack()
t.loaddir('textures')

# read image
i = Image.open('FastGhastBlast.png').convert("RGB")
