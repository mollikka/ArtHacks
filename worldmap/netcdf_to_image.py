from math import sqrt,pi
from PIL import Image, ImageDraw

from netCDF4 import Dataset

f = Dataset("GEBCO_2014_2D.nc","r")

DATA_LAT_RESOLUTION = len(f.variables['lat'])
DATA_LON_RESOLUTION = len(f.variables['lon'])

PICTURE_X_RESOLUTION = 400
PICTURE_Y_RESOLUTION = 200

PICTURE_X_CHUNKS = 1
PICTURE_Y_CHUNKS = 1

PICTURE_X_RESOLUTION_PER_CHUNK = int(PICTURE_X_RESOLUTION / PICTURE_X_CHUNKS)
PICTURE_Y_RESOLUTION_PER_CHUNK = int(PICTURE_Y_RESOLUTION / PICTURE_Y_CHUNKS)

Y_MIN = -90
Y_MAX = 90

Y_RANGE = Y_MAX - Y_MIN

X_MIN = -180 * 3/2 * sqrt(1/3)
X_MAX = 180 * 3/2 * sqrt(1/3)

X_RANGE = X_MAX - X_MIN

ELEVATION_MIN = -8000
ELEVATION_MAX = 8000

ELEVATION_RANGE = ELEVATION_MAX - ELEVATION_MIN

def get_elevation(lat, lon):
    lat_data = round((lat+90)/180*DATA_LAT_RESOLUTION)
    lon_data = round((lon+180)/360*DATA_LON_RESOLUTION)
    if not ((0 <= lat_data) and (lat_data < DATA_LAT_RESOLUTION)):
        return ELEVATION_MIN
    if not ((0 <= lon_data) and (lon_data < DATA_LON_RESOLUTION)):
        return ELEVATION_MIN
    elev = f.variables["elevation"][DATA_LAT_RESOLUTION-lat_data-1][lon_data]
    return min(ELEVATION_MAX, max(ELEVATION_MIN, elev))

def kavrayskiy_VII(x, y):
    y_rad = y*pi/180
    x_rad = x*pi/180
    lat = y_rad
    lon = 2/3 * x_rad * 1/sqrt(1/3 - y_rad**2/pi**2)
    return lat*180/pi, lon*180/pi

def cylindrical(x, y):
    lat = y
    lon = x
    return lat, lon

for chunk_x in range(PICTURE_X_CHUNKS):
    for chunk_y in range(PICTURE_Y_CHUNKS):
        print("Rendering chunk {},{}".format(chunk_x, chunk_y))

        map_image = Image.new("RGB", (PICTURE_X_RESOLUTION_PER_CHUNK, PICTURE_Y_RESOLUTION_PER_CHUNK))
        draw = ImageDraw.Draw(map_image)

        for x in range(PICTURE_X_RESOLUTION_PER_CHUNK):
            for y in range(PICTURE_Y_RESOLUTION_PER_CHUNK):

                #chunk coordinates to full picture coordinates
                real_x = chunk_x*PICTURE_X_RESOLUTION_PER_CHUNK + x
                real_y = chunk_y*PICTURE_Y_RESOLUTION_PER_CHUNK + y

                #picture coordinates to model coordinates
                i = X_MIN + real_x/(PICTURE_X_RESOLUTION-1)*X_RANGE
                j = Y_MIN + real_y/(PICTURE_Y_RESOLUTION-1)*Y_RANGE
                try:
                    #model pixel to earth coordinates
                    lat,lon = kavrayskiy_VII(i,j)
                    #lat,lon = cylindrical(i,j)
                    #earth coordinates to elevation
                    elev = get_elevation(lat,lon)
                except ValueError:
                    elev = ELEVATION_MIN
                #elevation to picture color value
                elev_color = int((elev - ELEVATION_MIN)/ELEVATION_RANGE*255)
                #draw it
                #print("picture {:3d},{:3d}\tcoordinates {: 4.3f},{: 4.3f}\televation {:5d}\telev color {:3d}".format(x,y,lat,lon,elev,elev_color))
                draw.point((x,y), (elev_color, elev_color, elev_color))
        map_image.save("map_{}_{}.png".format(chunk_x, chunk_y))
