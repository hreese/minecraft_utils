#!/usr/bin/python

from PIL import Image
from colormath.color_objects import *
import re
import os
import cStringIO
import operator
import base64

re_sideonly = re.compile('_side|_front')
re_toponly = re.compile('_top')

class Texture(object):
    """Minecraft texture"""
    def __init__(self):
        self.tags = {}
        self.cache = {}

    def loadfile(self, filename):
        # keep filename
        self._filename = filename

        with open(filename, 'r') as file:
            # keep original image
            self.rawimage = file.read(-1)

        # TODO: need better 'heuristics'
        self.format = 'png'

        # keep PIL RGB version
        self.image = Image.open(cStringIO.StringIO(self.rawimage)).convert("RGB")

        # shrink image to obtain single color
        self.singlecolor = self.image.resize( (1,1), resample=Image.ANTIALIAS).getpixel( (0,0) )

        # convert to Lab colorspace for better comparison
        self.rgbcolor = RGBColor(*self.singlecolor, rgb_type='sRGB')
        self.labcolor = self.rgbcolor.convert_to('lab')

        # tag
        # FIXME: logs and pillars can be placed vertically
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

#   def __str__(self):
#       return self.filename
#   def __repr__(self):
#       return self.filename

    @property
    def base64(self):
        """base64 encoded version for HTML embedding"""
        if not self.cache.has_key('base64'):
            self.cache['base64'] = base64.b64encode(self.rawimage).replace("\n", "")
        return self.cache['base64']

    @property
    def datauri(self):
        return "data:image/%s;base64,%s" % (self.format, self.base64)

    @property
    def filename(self):
        return self._filename

    @property
    def html_img(self):
        (w, h) = self.image.size
        return '<img width="%d" height="%d" alt="%s" id="%s" src="%s" />' % (w, h, self.filename, self.filename, self.datauri)

class TexturePack(object):
    """Collection of textures"""
    def __init__(self):
        self._textures = {}
        self._match_cache = {}

    @property
    def textures(self):
        return self._textures

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
                        self._textures[filename] = t
                    except IOError:
                        pass

    def getMatches(self, color):
        """Return dictionary mapping distance (== similarity) to textures"""
        assert not isinstance(color, basestring), "color is not an RGB tuple"

        if not self._match_cache.has_key(color):
            matches = {}
            labcolor = RGBColor(*color, rgb_type='sRGB').convert_to('lab')
            for t in self.textures.values():
                matches[t] = t.labcolor.delta_e(labcolor)
            self._match_cache[color] = matches

        return self._match_cache[color]

    def getSortedMatches(self, color):
        """Return textures sorted by distance"""
        matches = self.getMatches(color)
        return matches # TODO: FIXME
        #return sorted(matches.iteritems(), key=operator.itemgetter(0))

#   def getSortedMatches(self, color):
#       """Return textures sorted by distance"""
#       matches = self.getMatches(color)
#       return OrderedDict(sorted(matches.items(), key=lambda t: t[1], reverse=False))

# testing

# load texture pack
tp = TexturePack()
tp.loaddir('textures')

t = Texture()
t.loadfile('textures/blocks/obsidian.png')

# read image
i = Image.open('FastGhastBlast.png').convert("RGB")
for w in xrange(0, i.size[0]-1):
    for h in xrange(0, i.size[1]-1):
        color = i.getpixel((w,h))
        m = tp.getMatches(color)
        print "<!-- [%3d, %3d]: (%d, %d, %d) --> %s" % (h, w, color[0], color[1], color[2], m.keys()[0])

    print "<br>"
