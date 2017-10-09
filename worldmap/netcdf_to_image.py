from math import sqrt,pi
from PIL import Image, ImageDraw

from netCDF4 import Dataset

f = Dataset("GEBCO_2014_2D.nc","r")

DATA_LAT_RESOLUTION = len(f.variables['lat'])
DATA_LON_RESOLUTION = len(f.variables['lon'])

ELEVATION_MIN = -8000
ELEVATION_MAX = 8000

ELEVATION_RANGE = ELEVATION_MAX - ELEVATION_MIN

Y_MIN = -90
Y_MAX = 90

Y_RANGE = Y_MAX - Y_MIN

X_MIN = -180 * 3/2 * sqrt(1/3)
X_MAX = 180 * 3/2 * sqrt(1/3)

X_RANGE = X_MAX - X_MIN

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


def picture_coordinates_to_elevation(x_resolution, y_resolution, real_x, real_y):

    try:
        lat,lon = picture_coordinates_to_earth_coordinates(
                x_resolution, y_resolution, real_x, real_y)
        elev = get_elevation(lat,lon)
    except ValueError:
        elev = ELEVATION_MIN
    return elev

def picture_coordinates_to_earth_coordinates(x_resolution, y_resolution, real_x, real_y):

    #warning: can throw ValueError if outside the projection

    #picture coordinates to model coordinates
    i = X_MIN + real_x/(x_resolution-1)*X_RANGE
    j = Y_MIN + real_y/(y_resolution-1)*Y_RANGE
    #model pixel to earth coordinates
    lat,lon = kavrayskiy_VII(i,j)
    return lat,lon


def pixel_chunk_mode(x_resolution_per_chunk, y_resolution_per_chunk,
                        x_chunk_count, y_chunk_count):

    PICTURE_X_RESOLUTION_PER_CHUNK = x_resolution_per_chunk
    PICTURE_Y_RESOLUTION_PER_CHUNK = y_resolution_per_chunk
    PICTURE_X_CHUNKS = x_chunk_count
    PICTURE_Y_CHUNKS = y_chunk_count
    PICTURE_X_RESOLUTION = x_chunk_count * x_resolution_per_chunk
    PICTURE_Y_RESOLUTION = y_chunk_count * y_resolution_per_chunk

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

                    elev = picture_coordinates_to_elevation(PICTURE_X_RESOLUTION, PICTURE_Y_RESOLUTION, real_x, real_y)

                    #elevation to picture color value
                    elev_color = int((elev - ELEVATION_MIN)/ELEVATION_RANGE*255)
                    #draw it
                    draw.point((x,y), (elev_color, elev_color, elev_color))
            map_image.save("map_{}_{}.png".format(chunk_x, chunk_y))

def angle_chunk_mode(x_resolution, y_resolution,
        latitude_chunk_count, longitude_chunk_count):

    def chunk_index(lat,lon):
        return longitude_chunk_count*lat + lon

    PICTURE_X_RESOLUTION = x_resolution
    PICTURE_Y_RESOLUTION = y_resolution

    chunk_image = [None]*latitude_chunk_count*longitude_chunk_count
    chunk_draw = [None]*latitude_chunk_count*longitude_chunk_count

    LATITUDE_PER_CHUNK = 180/latitude_chunk_count
    LONGITUDE_PER_CHUNK = 360/longitude_chunk_count

    MIN_LATITUDE = -90
    MIN_LONGITUDE = -180

    for chunk_lat in range(latitude_chunk_count):
        for chunk_lon in range(longitude_chunk_count):
            image = Image.new("RGB", (PICTURE_X_RESOLUTION, PICTURE_Y_RESOLUTION))
            draw = ImageDraw.Draw(image)
            chunk_image[chunk_index(chunk_lat, chunk_lon)] = image
            chunk_draw[chunk_index(chunk_lat, chunk_lon)] = draw


    for x in range(PICTURE_X_RESOLUTION):
        for y in range(PICTURE_Y_RESOLUTION):

            lat,lon = picture_coordinates_to_earth_coordinates(
                    PICTURE_X_RESOLUTION, PICTURE_Y_RESOLUTION, x, y)

            for chunk_lat in range(latitude_chunk_count):
                for chunk_lon in range(longitude_chunk_count):

                    chunk_min_lat = chunk_lat*LATITUDE_PER_CHUNK + MIN_LATITUDE
                    chunk_max_lat = (chunk_lat+1)*LATITUDE_PER_CHUNK + MIN_LATITUDE
                    chunk_min_lon = chunk_lon*LONGITUDE_PER_CHUNK + MIN_LONGITUDE
                    chunk_max_lon = (chunk_lon+1)*LONGITUDE_PER_CHUNK + MIN_LONGITUDE

                    if not ((chunk_min_lat <= lat) and (lat <= chunk_max_lat)):
                        continue

                    if not ((chunk_min_lon <= lon) and (lon <= chunk_max_lon)):
                        continue

                    elev = get_elevation(lat,lon)

                    draw = chunk_draw[chunk_index(chunk_lat, chunk_lon)]

                    #elevation to picture color value
                    elev_color = int((elev - ELEVATION_MIN)/ELEVATION_RANGE*255)
                    #draw it
                    draw.point((x,y), (elev_color, elev_color, elev_color))

    for chunk_lat in range(latitude_chunk_count):
        for chunk_lon in range(longitude_chunk_count):
            chunk_image[chunk_index(chunk_lat, chunk_lon)].save("map_{}_{}.png".format(chunk_lat, chunk_lon))

if __name__ == "__main__":

    #pixel_chunk_mode(100,50,2,2)
    angle_chunk_mode(300,150,3,3)
