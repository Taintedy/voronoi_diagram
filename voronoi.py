import numpy
from edges import edge


class voronoi_graph:

    def __init__(self, triangles):
        self.voronoi_nodes = []
        self.voronoi_edges = []
        self.triagle_arr = triangles

    def dist(self, a, b):
        return numpy.sqrt((b.x - a.x) * (b.x - a.x) + (b.y - a.y) * (b.y - a.y))

    def get_neighbour_triangles(self, triangle, index):
        neighbours = []
        count = 0
        triangle_points = [triangle.point1, triangle.point2, triangle.point3]
        for i in range(0, len(self.triagle_arr)):
            if i != index:
                for j in range(0, 3):
                    if (triangle_points[j] == self.triagle_arr[i].point1) | (triangle_points[j] == self.triagle_arr[i].point2) | (triangle_points[j] == self.triagle_arr[i].point3):
                        count = count+1
                if count >= 2:
                    neighbours.append(self.triagle_arr[i])
                    count = 0
            count = 0
        return neighbours

    def vg_build(self):
        for i in self.triagle_arr:
            self.voronoi_nodes.append(i.cirCoords)
            neighbours = self.get_neighbour_triangles(i, self.triagle_arr.index(i))
            for l in neighbours:
                self.voronoi_edges.append(edge(i.cirCoords, l.cirCoords))
        return self.voronoi_edges
