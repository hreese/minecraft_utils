#!/usr/binenv python3

import zipfile
from PIL import Image,ImageChops,ImageOps
import io

location = {
    'potion_bottle_drinkable': 'assets/minecraft/textures/items/potion_bottle_drinkable.png',
    'potion_bottle_splash': 'assets/minecraft/textures/items/potion_bottle_splash.png',
    'potion_bottle_empty': 'assets/minecraft/textures/items/potion_bottle_empty.png',
    'potion_overlay': 'assets/minecraft/textures/items/potion_overlay.png'
}

images = {}

texturepackfile = 'faithful32pack.zip'

with zipfile.ZipFile(texturepackfile) as z:
    for i in location:
        images[i] = Image.open( io.BytesIO( z.open(location[i]).read()))

def tint_mask(mask, color = (1,0,0)):
    r, g, b, alpha = mask.split()
    graymask = ImageOps.grayscale(mask)
    coloredmask = ImageOps.colorize(graymask, (0,0,0), (255,0,0))
    coloredmask.putalpha(alpha)
    return coloredmask
