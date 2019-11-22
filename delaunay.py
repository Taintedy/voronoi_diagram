from edges import edge
from triangles import triangle
from points import point
import pygame


class delaunay:
    BLACK = (0, 0, 0)

    def __init__(self, points, sc):
        self.pointArr = points
        self.edgeArr = []
        self.triangleArr = []
        self.sc = sc
        self.superP1 = 0
        self.superP2 = 0
        self.superP3 = 0

    def superTriangle(self, points):
        maxX = points[0].x
        maxY = points[0].y
        minX = points[0].x
        minY = points[0].y

        for i in range(0, len(points)):
            if points[i].x < minX:
                minX = points[i].x
            if points[i].x > maxX:
                maxX = points[i].x
            if points[i].y < minY:
                minY = points[i].y
            if points[i].y > maxY:
                maxY = points[i].y

        dx = maxX - minX
        dy = maxY - minY
        deltaMax = max(dx, dy)
        midX = (minX + maxX) / 2
        midY = (minY + maxY) / 2
        self.superP1 = point(midX - 20* deltaMax, midY - deltaMax)
        self.superP2 = point(midX, midY + 20 * deltaMax)
        self.superP3 = point(midX + 20 * deltaMax, midY - deltaMax)
        # self.pointArr.append(self.superP1)
        # self.pointArr.append(self.superP2)
        # self.pointArr.append(self.superP3)
        self.triangleArr.append(triangle(self.superP1, self.superP2, self.superP3, self.sc))

    def drawTriangles(self, tri):
        # randColor = (random.randrange(0, 255, 1), random.randrange(0, 255, 1), random.randrange(0, 255, 1))
        WHITE = (25, 25, 25)
        pygame.draw.line(self.sc, WHITE, (tri.point1.x, tri.point1.y), (tri.point2.x, tri.point2.y), 1)
        pygame.draw.line(self.sc, WHITE, (tri.point2.x, tri.point2.y), (tri.point3.x, tri.point3.y), 1)
        pygame.draw.line(self.sc, WHITE, (tri.point3.x, tri.point3.y), (tri.point1.x, tri.point1.y), 1)

    def drawPoints(self, p):
        # randColor = (random.randrange(0, 255, 1), random.randrange(0, 255, 1), random.randrange(0, 255, 1))
        WHITE = (255, 255, 255)
        pygame.draw.circle(self.sc, WHITE, (int(p.x), int(p.y)), 5)

    def drawCircle(self, p,r):
        # randColor = (random.randrange(0, 255, 1), random.randrange(0, 255, 1), random.randrange(0, 255, 1))
        RED = (255, 0, 0)
        pygame.draw.circle(self.sc, RED, (int(p.x), int(p.y)), int(r), 1)

    def drawEdge(self, e):
        RED = (255, 0, 0)
        pygame.draw.line(self.sc, RED, (e.point1.x, e.point1.y), (e.point2.x, e.point2.y), 2)

    def chekDoubly(self, e):
        for i in range(0, len(e)):
            for j in range(i + 1, len(e)):
                if ((e[i].point1 == e[j].point1) & (e[i].point2 == e[j].point2)) | (
                        (e[i].point1 == e[j].point2) & (e[i].point2 == e[j].point1)):
                    e[i].isBad = 1
                    e[j].isBad = 1
                    break

    def formatPoints(self):
        self.pointArr.sort(key=lambda p: p.x)
        for l in range(0, len(self.pointArr) - 1):
            for j in range(l + 1, len(self.pointArr)):
                if self.pointArr[l].theSame(self.pointArr[j]):
                    self.pointArr[j].isBad = 1
        self.pointArr = [i for i in self.pointArr if i.isBad == 0]

    def triangulate(self):
        self.formatPoints()
        self.superTriangle(self.pointArr)
        for p in self.pointArr:
            self.drawPoints(p)
        for p in self.pointArr:
            # BLUE = (0, 0, 255)
            # pygame.draw.circle(self.sc, BLUE, (int(p.x), int(p.y)), 5)
            # pygame.display.update()
            for t in self.triangleArr:
                if t.circumcircleContains(p):
                    t.isBad = 1
                    self.edgeArr.append(edge(t.point1, t.point2))
                    self.edgeArr.append(edge(t.point2, t.point3))
                    self.edgeArr.append(edge(t.point3, t.point1))
            self.triangleArr = [i for i in self.triangleArr if i.isBad == 0]
            self.chekDoubly(self.edgeArr)
            self.edgeArr = [i for i in self.edgeArr if i.isBad == 0]
            for e in self.edgeArr:
                self.triangleArr.append(triangle(e.point1, e.point2, p, self.sc))
            #self.triangleArr = [i for i in self.triangleArr if i.isBad == 0]
            # self.sc.fill(self.BLACK)
            # pygame.display.update()
            self.edgeArr = []
            # for t in self.triangleArr:
            #     self.sc.fill(self.BLACK)
            #     pygame.display.update()
            #     self.drawTriangles(t)
            #     self.drawCircle(t.cirCoords, t.radius)
            #     pygame.display.update()
            #     pygame.time.delay(1000)
            # for t in self.triangleArr:
            #     self.drawTriangles(t)

        # self.triangleArr = [i for i in self.triangleArr if not ((i.contains(self.superP1)) |
        #                                                         (i.contains(self.superP2)) |
        #                                                         (i.contains(self.superP3)))]

        for t in self.triangleArr:
            self.drawTriangles(t)

        return self.triangleArr

    # def add_to_triangle(self, p):
    #         for t in self.triangleArr:
    #             if t.circumcircleContains(p):
    #                 t.isBad = 1
    #                 self.edgeArr.append(edge(t.point1, t.point2))
    #                 self.edgeArr.append(edge(t.point2, t.point3))
    #                 self.edgeArr.append(edge(t.point3, t.point1))
    #         self.triangleArr = [i for i in self.triangleArr if i.isBad == 0]
    #         self.chekDoubly(self.edgeArr)
    #         self.edgeArr = [i for i in self.edgeArr if i.isBad == 0]
    #         for e in self.edgeArr:
    #             self.triangleArr.append(triangle(e.point1, e.point2, p, self.sc))
    #         #self.triangleArr = [i for i in self.triangleArr if i.isBad == 0]
    #         # self.sc.fill(self.BLACK)
    #         # pygame.display.update()
    #         self.edgeArr = []
    #         # for t in self.triangleArr:
    #         #     self.sc.fill(self.BLACK)
    #         #     pygame.display.update()
    #         #     self.drawTriangles(t)
    #         #     self.drawCircle(t.cirCoords, t.radius)
    #         #     pygame.display.update()
    #         #     pygame.time.delay(1000)
    #         # for t in self.triangleArr:
    #         #     self.drawTriangles(t)
    #
    #     # self.triangleArr = [i for i in self.triangleArr if not ((i.contains(self.superP1)) |
    #     #                                                         (i.contains(self.superP2)) |
    #     #                                                         (i.contains(self.superP3)))]
    #
    #         for t in self.triangleArr:
    #             self.drawTriangles(t)
    #
    #         return self.triangleArr

