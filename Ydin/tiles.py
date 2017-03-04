import sys
import random
from math import pi, sin, cos, sqrt, atan2, exp

import xml.etree.ElementTree as ET

class Plate:
    def __init__(self,x,y,rotation,size):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.size = size

    def svg(self):
        gon = 3

        sx = self.x
        sy = self.y

        pointlist = [(sx + self.size*sin((self.rotation/360.0+i)*2.0/gon*pi), sy + self.size*cos((self.rotation/360.0+i)*2.0/gon*pi)) for i in range(gon)]

        p = ET.Element("polygon")
        p.set("points", " ".join(["{},{}".format(*i) for i in pointlist]))
          
        return p

def build_plates(imagesize, z):
    plates = []
    modelsize = 30

    for x in range(-modelsize, modelsize+1):
        for y in range(-modelsize, modelsize+1):
            w = (sin(2.0/3*pi)/sin(2.0/12*pi))/2
            b = sqrt(1 - w**2)
            h = sqrt(w**2 - (w/2)**2)

            if y%2:
                xx,yy = 2*w*x + y*w/2, y*h
            else:
                xx,yy = 2*w*x + (y-1)*w/2 + w, (y-1)*h + b

            size = (2/3 * imagesize/modelsize *
                    min(1.1-0.06*sqrt((2*z)**2+(xx)**2+(yy)**2),1)
                    )
            if size < 5: size = 5

            x_img = xx*modelsize*imagesize/1000+imagesize/2
            y_img = yy*modelsize*imagesize/1000+imagesize/2
            
            if not ((0<x_img<imagesize) and (0<y_img<imagesize)): continue

            orientation = (y%2)*180 + 180
            plates.append(Plate(x_img, y_img, orientation,size))
    return plates

def make_svg(size,z):
    plates = build_plates(size,z)
    root = ET.Element("svg")
    root.set("width",str(size)), root.set("height",str(size))
    root.set("xmlns","http://www.w3.org/2000/svg")
    root.set("xmlns:xlink","http://www.w3.org/1999/xlink")
    edge = ET.SubElement(root,"polygon")
    edge.set("points", "0,0 0,1000 1000,1000 1000,0")
    edge.set("style", "stroke:red; fill:none;")
    for plate in plates: 
        p = plate.svg()
        if p is None: continue
        root.append(p)
    return ET.ElementTree(root)

if __name__ == "__main__":
    for z in range(7):
        make_svg(1000,z).write("layer_{}.svg".format(z))

