#!/usr/bin/env python
"""

voronoi2svg.py
Create Voronoi diagram from seeds (midpoints of selected objects)

- Voronoi Diagram algorithm and C code by Steven Fortune, 1987, http://ect.bell-labs.com/who/sjf/
- Python translation to file voronoi.py by Bill Simons, 2005, http://www.oxfish.com/

Copyright (C) 2011 Vincent Nivoliers and contributors

Contributors
  ~suv, <suv-sf@users.sf.net>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""
# standard library
import sys
import os
# local library
import inkex
import simplestyle
import simplepath
import simpletransform
import voronoi
import random

import math

import pytess

class Point:
  def __init__(self,x,y):
    self.x = x
    self.y = y

class Voronoi2svg(inkex.Effect):
  def __init__(self):
    inkex.Effect.__init__(self)

    #{{{ Additional options

    self.OptionParser.add_option(
      "--tab",
      action="store",
      type="string",
      dest="tab")
    self.OptionParser.add_option(
      '--diagram-type',
      action = 'store',
      type = 'choice', choices=['Voronoi','Delaunay'],
      default = 'Voronoi',
      dest='diagramType',
      help = 'Defines the type of the diagram')
    self.OptionParser.add_option(
      '--clip-box',
      action = 'store',
      type = 'choice', choices=['Page','Automatic from seeds'],
      default = 'Page',
      dest='clipBox',
      help = 'Defines the bounding box of the Voronoi diagram')
    self.OptionParser.add_option(
      '--show-clip-box',
      action = 'store',
      type = 'inkbool',
      default = False,
      dest='showClipBox',
      help = 'Set this to true to write the bounding box')
    self.OptionParser.add_option(
      '--delaunay-fill-options',
      action = 'store',
      type = 'string',
      default = "delaunay-no-fill",
      dest='delaunayFillOptions',
      help = 'Set the Delaunay triangles color options')
    self.OptionParser.add_option(
      '--break-into-triangles',
      action = 'store',
      type = 'inkbool',
      default = False,
      dest='breakIntoTriangles',
      help = 'Break Voronoi cells into triangles')
   #}}}

  #{{{ Clipping a line by a bounding box
  def dot(self,x,y):
    return x[0]*y[0] + x[1]*y[1]

  def intersectLineSegment(self,line,v1,v2):
    s1 = self.dot(line,v1) - line[2]
    s2 = self.dot(line,v2) - line[2]
    if s1*s2 > 0:
      return (0,0,False)
    else:
      tmp = self.dot(line,v1)-self.dot(line,v2)
      if tmp == 0:
        return(0,0,False)
      u = (line[2]-self.dot(line,v2))/tmp
      v = 1-u
      return (u*v1[0]+v*v2[0],u*v1[1]+v*v2[1],True)
  
  def clipEdge(self,vertices, lines, edge, bbox):
    #bounding box corners
    bbc = []
    bbc.append((bbox[0],bbox[2]))
    bbc.append((bbox[1],bbox[2]))
    bbc.append((bbox[1],bbox[3]))
    bbc.append((bbox[0],bbox[3]))

    #record intersections of the line with bounding box edges
    line = (lines[edge[0]])
    interpoints = []
    for i in range(4):
      p = self.intersectLineSegment(line,bbc[i],bbc[(i+1)%4])
      if (p[2]):
        interpoints.append(p)

    #if the edge has no intersection, return empty intersection
    if (len(interpoints)<2):
      return []

    if (len(interpoints)>2): #happens when the edge crosses the corner of the box
      interpoints = list(set(interpoints)) #remove doubles

    #points of the edge
    v1 = vertices[edge[1]]
    interpoints.append((v1[0],v1[1],False))
    v2 = vertices[edge[2]]
    interpoints.append((v2[0],v2[1],False))

    #sorting the points in the widest range to get them in order on the line
    minx = interpoints[0][0]
    maxx = interpoints[0][0]
    miny = interpoints[0][1]
    maxy = interpoints[0][1]
    for point in interpoints:
      minx = min(point[0],minx)
      maxx = max(point[0],maxx)
      miny = min(point[1],miny)
      maxy = max(point[1],maxy)

    if (maxx-minx) > (maxy-miny):
      interpoints.sort()
    else:
      interpoints.sort(key=lambda pt: pt[1])

    start = []
    inside = False #true when the part of the line studied is in the clip box
    startWrite = False #true when the part of the line is in the edge segment
    for point in interpoints:
      if point[2]: #The point is a bounding box intersection
        if inside:
          if startWrite:
            return [[start[0],start[1]],[point[0],point[1]]]
          else:
            return []
        else: 
          if startWrite:
            start = point
        inside = not inside
      else: #The point is a segment endpoint
        if startWrite:
          if inside:
            #a vertex ends the line inside the bounding box
            return [[start[0],start[1]],[point[0],point[1]]]
          else:
            return []
        else:
          if inside:
            start = point
        startWrite = not startWrite
          
  #}}}

  #{{{ Transformation helpers

  def getGlobalTransform(self,node):
    parent = node.getparent()
    myTrans = simpletransform.parseTransform(node.get('transform'))
    if myTrans:
      if parent is not None:
        parentTrans = self.getGlobalTransform(parent)
        if parentTrans:
          return simpletransform.composeTransform(parentTrans,myTrans)
        else:
          return myTrans
    else:
      if parent is not None:
        return self.getGlobalTransform(parent)
      else:
        return None
    

  #}}}

  def effect(self):
    #saveout = sys.stdout
    #sys.stdout = sys.stderr
    #{{{ Check that elements have been selected

    if len(self.options.ids) == 0:
      inkex.errormsg(_("Please select objects!"))
      return

    #}}}

    #{{{ Drawing styles
    
    brokentrianglestyle = {
        'stroke'          : '#000000',
        'stroke-width'    : str(self.unittouu('1px')),
        'fill'            : 'none',
        'stroke-linecap'  : 'round',
        'stroke-linejoin' : 'round'
        }

    linestyle = {
        'stroke'          : '#000000',
        'stroke-width'    : str(self.unittouu('2px')),
        'fill'            : 'none',
        'stroke-linecap'  : 'round',
        'stroke-linejoin' : 'round'
        }
    
    facestyle = {
        'stroke'          : '#000000',
        'stroke-width'    : str(self.unittouu('1px')),
        'fill'            : 'none',
        'stroke-linecap'  : 'round',
        'stroke-linejoin' : 'round'
        }

    #}}}

    #{{{ Handle the transformation of the current group
    parentGroup = self.getParentNode(self.selected[self.options.ids[0]])

    trans = self.getGlobalTransform(parentGroup)
    invtrans = None
    if trans:
      invtrans = simpletransform.invertTransform(trans)

    #}}}

    #{{{ Recovery of the selected objects

    pts = []
    nodes = []
    seeds = []
    fills = []


    for id in self.options.ids:
      node = self.selected[id]
      nodes.append(node)
      bbox = simpletransform.computeBBox([node])
      if bbox:
        cx = 0.5*(bbox[0]+bbox[1])
        cy = 0.5*(bbox[2]+bbox[3])
        pt = [cx,cy]
        if trans:
          simpletransform.applyTransformToPoint(trans,pt)
        pts.append(Point(pt[0],pt[1]))
        fill = 'none'
        if self.options.delaunayFillOptions != "delaunay-no-fill":
            if 'style' in node.attrib:
                style = node.get('style') # fixme: this will break for presentation attributes!
                if style:
                    declarations = style.split(';')
                    for i,decl in enumerate(declarations):
                        parts = decl.split(':', 2)
                        if len(parts) == 2:
                            (prop, val) = parts
                            prop = prop.strip().lower()
                            if prop == 'fill':
                                fill = val.strip()
            fills.append(fill)
        seeds.append(Point(cx,cy))

    #}}}

    #{{{ Creation of groups to store the result

    # Voronoi
    groupVoronoi = inkex.etree.SubElement(parentGroup,inkex.addNS('g','svg'))
    groupVoronoi.set(inkex.addNS('label', 'inkscape'), 'Voronoi')
    if invtrans:
      simpletransform.applyTransformToNode(invtrans,groupVoronoi)

    if self.options.breakIntoTriangles and self.options.diagramType == 'Voronoi':
      groupBrokenTriangles = inkex.etree.SubElement(parentGroup,inkex.addNS('g','svg'))
      groupBrokenTriangles.set(inkex.addNS('label', 'inkscape'), 'Broken into triangles')
    #}}}

    #{{{ Clipping box handling

    #Clipping bounding box creation
    gBbox = simpletransform.computeBBox(nodes)

    #Clipbox is the box to which the Voronoi diagram is restricted
    clipBox = ()
    if self.options.clipBox == 'Page':
      svg = self.document.getroot()
      w = self.unittouu(svg.get('width'))
      h = self.unittouu(svg.get('height'))
      clipBox = (0,w,0,h)
    else:
      clipBox = (2*gBbox[0]-gBbox[1],
                 2*gBbox[1]-gBbox[0],
                 2*gBbox[2]-gBbox[3],
                 2*gBbox[3]-gBbox[2])
    
    #Safebox adds points so that no Voronoi edge in clipBox is infinite
    safeBox = (2*clipBox[0]-clipBox[1],
               2*clipBox[1]-clipBox[0],
               2*clipBox[2]-clipBox[3],
               2*clipBox[3]-clipBox[2])
    pts.append(Point(safeBox[0],safeBox[2]))
    pts.append(Point(safeBox[1],safeBox[2]))
    pts.append(Point(safeBox[1],safeBox[3]))
    pts.append(Point(safeBox[0],safeBox[3]))

    if self.options.showClipBox:
      #Add the clip box to the drawing
      rect = inkex.etree.SubElement(groupVoronoi,inkex.addNS('rect','svg'))
      rect.set('x',str(clipBox[0]))
      rect.set('y',str(clipBox[2]))
      rect.set('width',str(clipBox[1]-clipBox[0]))
      rect.set('height',str(clipBox[3]-clipBox[2]))
      rect.set('style',simplestyle.formatStyle(linestyle))

    #}}}

    #{{{ Voronoi diagram generation

    points = [(p.x, p.y) for p in pts] #convert to pytess format
    
    if self.options.diagramType == 'Voronoi':
      voronoipolygons = pytess.voronoi(points)
      
      voronoipoints = [i[0] for i in voronoipolygons if not i[0] is None]
      voronoipolygons = [i[1] for i in voronoipolygons if not i[0] is None]
    
    if self.options.diagramType == 'Delaunay':
      voronoipolygons = pytess.triangulate(points)

    for j,polygon in enumerate(voronoipolygons):

      point0 = polygon[0]
      cmds = [['M',[point0[0],point0[1]]]] # starting position
      for point in polygon[1:]:
        cmds.append(['L',[point[0], point[1]]]) # line to next point
      cmds.append(['Z',[]]) #close path

      #create path
      path = inkex.etree.Element(inkex.addNS('path','svg'))
      path.set('d',simplepath.formatPath(cmds))
      path.set('style',simplestyle.formatStyle(linestyle))
      groupVoronoi.append(path)

      if self.options.breakIntoTriangles and self.options.diagramType == 'Voronoi':

        point_x = [i[0] for i in polygon]
        point_y = [i[1] for i in polygon]
      
        path_neighbors = [((point_x[i],point_y[i]), (point_x[i-1],point_y[i-1])) for i in range(len(point_x))]


        for neighbor_pair in path_neighbors:
          point0 = voronoipoints[j]
          cmds = [['M',[point0[0],point0[1]]]] # starting position
          cmds.append(['L',[neighbor_pair[0][0], neighbor_pair[0][1]]]) # line to next point
          cmds.append(['L',[neighbor_pair[1][0], neighbor_pair[1][1]]])
          cmds.append(['Z',[]]) #close path


          #choose fragment color
          x = neighbor_pair[0][0] + neighbor_pair[1][0] - point0[0]*2
          y = neighbor_pair[0][1] + neighbor_pair[1][1] - point0[1]*2
          angle = 180/math.pi * math.atan2(y,x) + 180
       
          #totuudensiemen
          '''
          if angle < 30:
            color = '#ff0000'
          elif angle < 150:
            color = '#00ff00'
          elif angle < 270:
            color = '#0000ff'
          else:
            color = '#ff0000'
          '''
          if angle < 90:
            color = '#00ff00'
          if angle < 180:
            color = '#ff0000'
          elif angle < 270:
            color = '#ffff00'
          else:
            color = '#00ffff'
          brokentrianglestyle['fill']= color

          #create path
          path = inkex.etree.Element(inkex.addNS('path','svg'))
          path.set('d',simplepath.formatPath(cmds))
          path.set('style',simplestyle.formatStyle(brokentrianglestyle))
          groupBrokenTriangles.append(path)

  def draw_SVG_path(self,points, style, parent):
                
    attribs = {
        'style'     : style,
        'd'         : "M "+" ".join("{:.6g},{:.6g}".format(*point) for point in points)  +" Z"
            }
    circ = inkex.etree.SubElement(parent, inkex.addNS('path','svg'), attribs )



if __name__ == "__main__":
  e = Voronoi2svg()
  e.affect()


# vim: expandtab shiftwidth=2 tabstop=2 softtabstop=2 fileencoding=utf-8 textwidth=99
