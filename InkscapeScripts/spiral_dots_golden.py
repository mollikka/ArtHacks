#!/usr/bin/env python

import math
import random
import inkex
import simplepath
import simpletransform
import simplestyle

phi = (1 + 5**0.5)/2 

class C(inkex.Effect):
  def __init__(self):
    inkex.Effect.__init__(self)

  def effect(self):

    parent = self.current_layer
    svg = self.document.getroot()

    width, height = self.unittouu(svg.get('width')), self.unittouu(svg.get('height'))
    #xmid, ymid = width/2, height/2
    xmid, ymid = 0,0
    
    pointcount = 150 #400

    self.draw_SVG_circle(4, (xmid, ymid), parent)
    
    for i in range(1,#20
            pointcount):
        
        angle = i * (2*math.pi)/phi
        #angle = angle * 2
        #angle = i 
        distance = (float(i)/pointcount) * (math.sqrt(2)*max([width,height])/2)
        xx = xmid + distance*math.sin(angle)
        yy = ymid + distance*math.cos(angle)
      
        #if ((0<xx) and (xx<width)) and ((0<yy) and (yy<height)):
        self.draw_SVG_circle(1, (xx, yy), parent)


  def get_center(self, path):
    point_x = [i[1][0] for i in path if i[1]]
    point_y = [i[1][1] for i in path if i[1]]
    return sum(point_x)/len(point_x), sum(point_y)/len(point_y)



  def draw_SVG_circle(self,r, (x,y), parent):

    style = {   'fill'          : '#000000'
            }
                
    attribs = {
        'style'     : simplestyle.formatStyle(style),
        'r'        : str(r),
        'cx'         : str(x),
        'cy'         : str(y)
            }
    circ = inkex.etree.SubElement(parent, inkex.addNS('circle','svg'), attribs )



if __name__ == '__main__':
  c = C()
  c.affect()



# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
