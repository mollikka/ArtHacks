from math import sqrt,pi
from PIL import Image, ImageDraw

from netCDF4 import Dataset

from meshobject import MeshObject

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
    return scale_elevation(elev)

def scale_elevation(elevation):
    clamped_elev = min(ELEVATION_MAX, max(ELEVATION_MIN, elevation))
    return (clamped_elev - ELEVATION_MIN)/ELEVATION_RANGE

def kavrayskiy_VII_inverse(x, y):
    y_rad = y*pi/180
    x_rad = x*pi/180
    lat = y_rad
    lon = 2/3 * x_rad * 1/sqrt(1/3 - y_rad**2/pi**2)
    return lat*180/pi, lon*180/pi

def kavrayskiy_VII(lat, lon):
    lat_rad = lat*pi/180
    lon_rad = lon*pi/180
    x = 3/2*lon_rad*sqrt(1/3 - (lat_rad/pi)**2)
    y = lat_rad
    return x, y


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
    lat,lon = kavrayskiy_VII_inverse(i,j)
    return lat,lon

def earth_coordinates_to_picture_coordinates(lat_resolution, lon_resolution, lat_y, lon_x):

    #lat_y [0,lat_resolution[
    #lon_x [0,lon_resolution[

    lat = lat_y/lat_resolution * 180 - 90
    lon = lon_x/lon_resolution * 360 - 180

    x,y = kavrayskiy_VII(lat, lon)
    return x,y

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

    PICTURE_X_RESOLUTION = x_resolution
    PICTURE_Y_RESOLUTION = y_resolution

    LATITUDE_PER_CHUNK = 180/latitude_chunk_count
    LONGITUDE_PER_CHUNK = 360/longitude_chunk_count

    MIN_LATITUDE = -90
    MIN_LONGITUDE = -180

    for chunk_lat in range(latitude_chunk_count):
        for chunk_lon in range(longitude_chunk_count):

            print("Rendering chunk {},{}".format(chunk_lat, chunk_lon))

            chunk_image = Image.new("RGB", (PICTURE_X_RESOLUTION, PICTURE_Y_RESOLUTION))
            chunk_draw = ImageDraw.Draw(chunk_image)

            for x in range(PICTURE_X_RESOLUTION):
                for y in range(PICTURE_Y_RESOLUTION):

                    lat,lon = picture_coordinates_to_earth_coordinates(
                            PICTURE_X_RESOLUTION, PICTURE_Y_RESOLUTION, x, y)

                    chunk_min_lat = chunk_lat*LATITUDE_PER_CHUNK + MIN_LATITUDE
                    chunk_max_lat = (chunk_lat+1)*LATITUDE_PER_CHUNK + MIN_LATITUDE
                    chunk_min_lon = chunk_lon*LONGITUDE_PER_CHUNK + MIN_LONGITUDE
                    chunk_max_lon = (chunk_lon+1)*LONGITUDE_PER_CHUNK + MIN_LONGITUDE

                    if not ((chunk_min_lat <= lat) and (lat <= chunk_max_lat)):
                        continue

                    if not ((chunk_min_lon <= lon) and (lon <= chunk_max_lon)):
                        continue

                    elev = get_elevation(lat,lon)

                    #elevation to picture color value
                    elev_color = int(elev*255)
                    #draw it
                    chunk_draw.point((x,y), (elev_color, elev_color, elev_color))

            chunk_image.save("map_{}_{}.png".format(chunk_lat, chunk_lon))


def angle_chunk_stl_mode(lat_resolution_per_chunk, lon_resolution_per_chunk,
        latitude_chunk_count, longitude_chunk_count):

    LAT_RESOLUTION_PER_CHUNK = lat_resolution_per_chunk
    LON_RESOLUTION_PER_CHUNK = lon_resolution_per_chunk

    LAT_RESOLUTION = LAT_RESOLUTION_PER_CHUNK*latitude_chunk_count
    LON_RESOLUTION = LON_RESOLUTION_PER_CHUNK*longitude_chunk_count

    LATITUDE_PER_CHUNK = 180/latitude_chunk_count
    LONGITUDE_PER_CHUNK = 360/longitude_chunk_count

    MIN_LATITUDE = -90
    MIN_LONGITUDE = -180

    def chunk_coords_to_x_y(chunk_lat, chunk_lon, lat, lon):
        r_lat = chunk_lat*LAT_RESOLUTION_PER_CHUNK + lat
        r_lon = chunk_lon*LON_RESOLUTION_PER_CHUNK + lon
        x,y = earth_coordinates_to_picture_coordinates(
            LAT_RESOLUTION, LON_RESOLUTION, r_lat, r_lon)

        return x,y

    def chunk_coords_to_real_lat_lon(chunk_lat, chunk_lon, lat, lon):
        real_lat = (chunk_lat*LAT_RESOLUTION_PER_CHUNK + lat)/LAT_RESOLUTION*180-90
        real_lon = (chunk_lon*LON_RESOLUTION_PER_CHUNK + lon)/LON_RESOLUTION*360-180
        return real_lat, real_lon

    def iterate_borders(chunk_lat, chunk_lon):

        lat = 0
        lon = 0

        for lat in range(LAT_RESOLUTION_PER_CHUNK):
            x, y = chunk_coords_to_x_y(chunk_lat, chunk_lon, lat, lon)
            real_lat, real_lon = chunk_coords_to_real_lat_lon(chunk_lat, chunk_lon, lat, lon)
            elev = get_elevation(real_lat, real_lon)
            yield x, y, scale_elevation(elev)
        lat+=1

        for lon in range(LON_RESOLUTION_PER_CHUNK):
            x, y = chunk_coords_to_x_y(chunk_lat, chunk_lon, lat, lon)
            real_lat, real_lon = chunk_coords_to_real_lat_lon(chunk_lat, chunk_lon, lat, lon)
            elev = get_elevation(real_lat, real_lon)
            yield x, y, scale_elevation(elev)
        lon+=1

        for lat in range(LAT_RESOLUTION_PER_CHUNK,0,-1):
            x, y = chunk_coords_to_x_y(chunk_lat, chunk_lon, lat, lon)
            real_lat, real_lon = chunk_coords_to_real_lat_lon(chunk_lat, chunk_lon, lat, lon)
            elev = get_elevation(real_lat, real_lon)
            yield x, y, scale_elevation(elev)
        lat-=1

        for lon in range(LON_RESOLUTION_PER_CHUNK,0,-1):
            x, y = chunk_coords_to_x_y(chunk_lat, chunk_lon, lat, lon)
            real_lat, real_lon = chunk_coords_to_real_lat_lon(chunk_lat, chunk_lon, lat, lon)
            elev = get_elevation(real_lat, real_lon)
            yield x, y, scale_elevation(elev)

        x, y = chunk_coords_to_x_y(chunk_lat, chunk_lon, 0, 0)
        real_lat, real_lon = chunk_coords_to_real_lat_lon(chunk_lat, chunk_lon, lat, lon)
        elev = get_elevation(real_lat, real_lon)
        yield x, y, scale_elevation(elev)

    for chunk_lat in range(latitude_chunk_count):
        for chunk_lon in range(longitude_chunk_count):

            borders = list(iterate_borders(chunk_lat, chunk_lon))

            height_map_vertex_count = 2 * LAT_RESOLUTION * LON_RESOLUTION
            borders_vertex_count = 2 * len(borders)
            bottom_vertex_count = len(borders)

            print("Rendering chunk {},{}".format(chunk_lat, chunk_lon))

            chunk_mesh = MeshObject(height_map_vertex_count +
                                    borders_vertex_count +
                                    bottom_vertex_count)

            print("Rendering height map")
            #height map
            for lat in range(LAT_RESOLUTION_PER_CHUNK):
                print(lat,"/",LAT_RESOLUTION_PER_CHUNK)
                for lon in range(LON_RESOLUTION_PER_CHUNK):

                    x1, y1 = chunk_coords_to_x_y(chunk_lat, chunk_lon, lat, lon)
                    real_lat, real_lon = chunk_coords_to_real_lat_lon(chunk_lat, chunk_lon, lat, lon)
                    elev1 = get_elevation(real_lat, real_lon)
                    p1 = x1, y1, elev1

                    x2, y2 = chunk_coords_to_x_y(chunk_lat, chunk_lon, lat+1, lon)
                    real_lat, real_lon = chunk_coords_to_real_lat_lon(chunk_lat, chunk_lon, lat+1, lon)
                    elev2 = get_elevation(real_lat, real_lon)
                    p2 = x2, y2, elev2

                    x3, y3 = chunk_coords_to_x_y(chunk_lat, chunk_lon, lat, lon+1)
                    real_lat, real_lon = chunk_coords_to_real_lat_lon(chunk_lat, chunk_lon, lat, lon+1)
                    elev3 = get_elevation(real_lat, real_lon)
                    p3 = x3, y3, elev3

                    x4, y4 = chunk_coords_to_x_y(chunk_lat, chunk_lon, lat+1, lon+1)
                    real_lat, real_lon = chunk_coords_to_real_lat_lon(chunk_lat, chunk_lon, lat+1, lon+1)
                    elev4 = get_elevation(real_lat, real_lon)
                    p4 = x4, y4, elev4

                    chunk_mesh.add_face(p1, p2, p3)
                    chunk_mesh.add_face(p2, p3, p4)

            print("Rendering borders")
            #border
            for b1, b2 in ((borders[i],borders[i-1]) for i in range(len(borders))):

                x1, y1, elev1 = b1

                x2, y2, elev2 = b2

                chunk_mesh.add_face((x1, y1, 0),
                                    (x2, y2, 0),
                                    (x1, y1, elev1))

                chunk_mesh.add_face((x2, y2, 0),
                                    (x2, y2, elev2),
                                    (x1, y1, elev1))

            print("Rendering bottom")
            #bottom
            mid_x = sum(i[0] for i in borders)/len(borders)
            mid_y = sum(i[1] for i in borders)/len(borders)

            for b1, b2 in ((borders[i],borders[i-1]) for i in range(len(borders))):

                chunk_mesh.add_face((b1[0], b1[1], 0),
                                    (b2[0], b2[1], 0),
                                    (mid_x, mid_y, 0))

            #what we just built was a mirror image apparently
            #this is the level of my coding standards right now:
            chunk_mesh.mesh.x *= -1

            fname = "map_{}_{}.stl".format(chunk_lat, chunk_lon)
            print("Saving",fname)
            chunk_mesh.save(fname)

if __name__ == "__main__":

    #pixel_chunk_mode(100,50,2,2)
    #angle_chunk_mode(400,200,4,2)
    angle_chunk_stl_mode(400,400,8,4)
