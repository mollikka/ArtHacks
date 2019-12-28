import numpy
from stl import mesh, Mode

from matplotlib import pyplot
from mpl_toolkits import mplot3d

class MeshObject:

    def __init__(self, vertexcount):

        self.data = numpy.zeros(vertexcount, dtype=mesh.Mesh.dtype)
        self.mesh = mesh.Mesh(self.data)
        self.vertexcount = vertexcount
        self.i = -1

        self.x_min = float('inf')
        self.x_max = float('-inf')
        self.y_min = float('inf')
        self.y_max = float('-inf')
        self.z_min = float('inf')
        self.z_max = float('-inf')

    def add_face(self, point1, point2, point3):

        self.x_min = min(self.x_min, point1[0], point2[0], point3[0])
        self.x_max = max(self.x_max, point1[0], point2[0], point3[0])
        self.y_min = min(self.y_min, point1[0], point2[0], point3[0])
        self.y_max = max(self.y_max, point1[0], point2[0], point3[0])
        self.z_min = min(self.z_min, point1[0], point2[0], point3[0])
        self.z_max = max(self.z_max, point1[0], point2[0], point3[0])

        if self.i+1 < self.vertexcount:
            self.i += 1
            self.data['vectors'][self.i] = numpy.array([
                [point1[0], point1[1], point1[2]],
                [point2[0], point2[1], point2[2]],
                [point3[0], point3[1], point3[2]]])
        else:
            raise MeshException("Too many faces")

    def save(self, stl_filename):

        self.mesh.save(stl_filename, mode=Mode.BINARY)

    def show(self):

        figure = pyplot.figure()
        axes = mplot3d.Axes3D(figure)

        axes.add_collection3d(mplot3d.art3d.Poly3DCollection(self.mesh.vectors))
        axes.auto_scale_xyz(self.mesh.points, self.mesh.points, self.mesh.points)

        pyplot.show()

    def center_x(self):

        new_x_max = (self.x_min + self.x_max)/2
        self.mesh.x += -self.x_min -new_x_max
        self.x_min = -new_x_max
        self.x_max = new_x_max

    def center_y(self):

        new_y_max = (self.y_min + self.y_max)/2
        self.mesh.y += -self.y_min -new_y_max
        self.y_min = -new_y_max
        self.y_max = new_y_max

    def center_z(self):

        new_z_max = (self.z_min + self.z_max)/2
        self.mesh.z += -self.z_min -new_z_max
        self.z_min = -new_z_max
        self.z_max = new_z_max

class MeshException(Exception):
    pass
