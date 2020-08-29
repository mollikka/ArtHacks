#!/usr/bin/env python

import math
import random
import inkex
import simplepath
import simpletransform
import simplestyle

class C(inkex.Effect):
  def __init__(self):
    inkex.Effect.__init__(self)

  def effect(self):

    #totuuden siemen
    colors = ['#005e70', '#f3a33b', '#b84b03','#dca6a9','#3a6b64']
    #colors = ['#130D24','#2a1b4a','#511b4a']
    #colors = ['#317bad','#47b6ff','#266087']
    #colors = ['#d740a0', '#802177','#331123']
              #light     #medium    #dark
    #colors = ['#3dadf2','#031ca6','#020f59']

    #colors = [  '#f20732',
    #            '#07038c', 
    #            '#0439d9',
    #            '#056cf2']
    #colors = ['red', 'blue', 'green']
    
    for myid, myitem in self.selected.iteritems():
      d = myitem.get( 'd' );
      path = simplepath.parsePath(d)

      point_x = [i[1][0] for i in path if i[1]]
      point_y = [i[1][1] for i in path if i[1]]
      
      path_neighbors = [((point_x[i],point_y[i]), (point_x[i-1],point_y[i-1])) for i in range(len(point_x))]

      avg_point = self.get_center(path);
      #A = []
      for neighbors in path_neighbors:
        
        style = simplestyle.parseStyle(myitem.get( 'style' ));
        #raise Exception(neighbors + (avg_point,))
        x = neighbors[0][0] + neighbors[1][0] - avg_point[0]*2
        y = neighbors[0][1] + neighbors[1][1] - avg_point[1]*2
        angle = 180/math.pi * math.atan2(y,x) + 180

        #point towards the sun
        #angle = (angle + 180 - 180/math.pi*math.atan2(avg_point[1], avg_point[0])) % 360

        #self.draw_SVG_circle(5, (x,y), self.current_layer)
        #A.append(angle)
        #if angle < 72:
        #  color = colors[0]
        #elif angle < 72*2:
        #  color = colors[1]
        #elif angle < 72*3:
        #  color = colors[2]
        #elif angle < 72*4:
        #  color = colors[3]
        #else:
        #  color = colors[4]
        
        #three color
       
        #totuudensiemen
        if angle < 30:
          color = colors[2]
        elif angle < 150:
          color = colors[0]
        elif angle < 270:
          color = colors[1]
        else:
          color = colors[2]
        
        #continuous
        a = int((1+math.cos(abs(angle-180)/180*math.pi))/2*255)
        color = 'rgb({},{},{})'.format(a,a,a)

        #four color

        #if angle < 90:
        #  color = '#00ff00'
        #elif angle < 180:
        #  color = '#ff0000'
        #elif angle < 270:
        #  color = '#ffff00'
        #else:
        #  color = '#00ffff'



        #if angle < 120:
        #  color = colors[0]
        #elif angle < 240:
        #  color = colors[1]
        #else:
        #  color = colors[2]

        style['fill'] = color
        self.draw_SVG_path(neighbors + (avg_point,), simplestyle.formatStyle(style), self.current_layer)
      #raise Exception(A)
  def draw_SVG_path(self,points, style, parent):
                
    attribs = {
        'style'     : style,
        'd'         : "M "+" ".join("{:.6g},{:.6g}".format(*point) for point in points)  +" Z"
            }
    circ = inkex.etree.SubElement(parent, inkex.addNS('path','svg'), attribs )

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
