#! /usr/bin/env python
# Extension by Ragnar Stiansen - Dec 2014

'''
Set stroke color same as fill color on objects.

Made in Dec  2014 by Ragnar Stiansen
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import inkex
import simplestyle
import copy
import coloreffect


class Colorgrad(coloreffect.ColorEffect):
    __version__ = "0.01"

    def __init__(self):
        inkex.Effect.__init__(self)

        self.OptionParser.add_option("--color_white",
            action="store", type="int",
            dest="color_white")
        self.OptionParser.add_option("--color_black",
            action="store", type="int",
            dest="color_black")

    def colmod(self, r, g, b):
        wh = self.options.color_white
        wh_r = ((wh >> 24) & 255)
        wh_g = ((wh >> 16) & 255)
        wh_b = ((wh >>  8) & 255)
        wh_hsl = self.rgb_to_hsl(wh_r/255.0, wh_g/255.0, wh_b/255.0)
        
        bl = self.options.color_black
        bl_r = ((bl >> 24) & 255)
        bl_g = ((bl >> 16) & 255)
        bl_b = ((bl >>  8) & 255)
        bl_hsl = self.rgb_to_hsl(bl_r/255.0, bl_g/255.0, bl_b/255.0)
      
        hsl = self.rgb_to_hsl(r/255.0, g/255.0, b/255.0)

        value = hsl[2]
        new_hsl = [wh_hsl[i] * (1-value) + bl_hsl[i] * (value) for i in range(len(hsl))]
        
        #force hue (angle) to interpolate the shorter distance!!
        h_dist = (bl_hsl[0] - wh_hsl[0]) % 1
        h_dist = 2*h_dist % 1 - h_dist
        new_hsl[0] = wh_hsl[0] + h_dist*value
        
        new_rgb = self.hsl_to_rgb(*new_hsl)
        #raise Exception(str(new_hsl) + '   ' + str(new_rgb))
        new_r, new_g, new_b = [int(i * 255) for i in new_rgb]

        return '%02x%02x%02x' % (new_r, new_g, new_b)
e = Colorgrad()
e.affect()
