#!/usr/bin/python

# get player's heasd skin and create a large (A3) printable PDF

from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A3,A4

import urllib2
import PIL
import sys
import io
from contextlib import closing

usernames = ['MineSprawl', 'dividuum', 'aykura', 'Labanane', 'FelixW80', 'Aachthor', 'JulianX4', 'vanyarw']

# head coords
skin_bb = {
    'head_left'  : (0,8,8,16),
    'head_front' : (8,8,16,16),
    'head_right' : (16,8,24,16),
    'head_back'  : (24,8,32,16),
    'head_top'   : (8,0,16,8),
}

# download skin
def get_mc_avatar(name = "MineSprawl"):
    with closing(urllib2.urlopen("http://skins.minecraft.net/MinecraftSkins/%s.png" % name)) as avatar_response:
        return PIL.Image.open( io.BytesIO(avatar_response.read()) )

# 25x25 (A3)

def create_pdf(username):
    c = canvas.Canvas("%s.pdf" % username, pagesize=A3)
    # todo: set metadata
    return c

def write_texture_to_page(c, texture, scalef=cm):
    # compensate for different coordinate systems
    texture = texture.transpose(PIL.Image.FLIP_TOP_BOTTOM)
    for x in xrange(texture.size[0]):
        for y in xrange(texture.size[1]):
            (r,g,b,a) = texture.getpixel((x,y))
            c.setFillColorRGB(r/256.,g/256.,b/256.)
            c.setStrokeColorRGB(r/256.,g/256.,b/256.)
            #print("Created rect at %d,%d with fill color %d,%d,%d" % (x, y, r, g, b))
            c.rect(scalef*x, scalef*y, scalef, scalef, stroke=1, fill=1)
    c.showPage()

def close_pdf(c):
    c.save()

for username in usernames:
    i=get_mc_avatar(username)
    c = create_pdf("large_head_%s" % username)
    for side in skin_bb.keys():
        c.drawString(2*cm, A3[1]-2*cm, "%s - %s" % (username, side))
        c.translate(2*cm, 5.5*cm)
        write_texture_to_page(c, i.crop(skin_bb[side]), 3.125*cm)
    close_pdf(c)

#def main(argv):
#    if len(argv) != 2:
#        sys.stderr.write("Usage: %s MineCraftUserName\n" % argv[0])
#        return 2
#    else:
#        username = argv[1]
#        create_pdf(username)
#
#if __name__ == "__main__":
#    sys.exit(main(sys.argv))
