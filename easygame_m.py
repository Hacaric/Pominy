from easygame import *

def bg_color(r,g,b):
    fill(r,g,b)

def draw_rect(posx, posy, width, height, colorm, ui = False):
    draw_polygon((posx, posy), (posx+width, posy), (posx+width, posy + height), (posx, posy + height), color = colorm, ui = ui)