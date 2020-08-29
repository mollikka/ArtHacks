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
    for myid, myitem in self.selected.iteritems():
      d = myitem.get( 'd' );
      path = simplepath.parsePath(d)
      avg_point = self.get_center(path)
      #path_points = [];
      #for segment in d.split():
      #  try:
      #    x,y = segment.split(',');
      #    path_points.append( (float(x), float(y)) );
      #  except ValueError:
      #    pass
      #avg_point = ( sum(i[0] for i in path_points)/len(path_points), 
      #              sum(i[1] for i in path_points)/len(path_points))
      self.draw_SVG_circle(1, (avg_point[0], avg_point[1]), self.current_layer)
  
  def draw_SVG_square(self,(w,h), (x,y), parent):

    style = {   'stroke'        : 'none',
                'stroke-width'  : '1',
                'fill'          : '#000000'
            }
                
    attribs = {
        'style'     : simplestyle.formatStyle(style),
        'height'    : str(h),
        'width'     : str(w),
        'x'         : str(x),
        'y'         : str(y)
            }
    circ = inkex.etree.SubElement(parent, inkex.addNS('rect','svg'), attribs )
  
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

  def get_center(self, path):
    point_x = [i[1][0] for i in path if i[1]]
    point_y = [i[1][1] for i in path if i[1]]
    return sum(point_x)/len(point_x), sum(point_y)/len(point_y)

if __name__ == '__main__':
  c = C()
  c.affect()



# vim: expandtab shiftwidth=4 tabstop=8 softtabstop=4 fileencoding=utf-8 textwidth=99
