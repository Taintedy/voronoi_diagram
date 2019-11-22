import pygame
from delaunay import delaunay
from points import point
from voronoi import voronoi_graph
from pygame.locals import *
import numpy
import random

FPS = 144
WIN_WIDTH = 1500
WIN_HEIGHT = 1000
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (75, 0, 130)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)
pygame.init()
points = []
for i in range(0, 10):
    points.append(point(1000,500-i*20 ))
    points.append(point(500-i*20,750))
    #points.append(point(numpy.random.normal(1500 / 2, 100), numpy.random.normal(1000 / 2, 100)))
clock = pygame.time.Clock()
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

while 1:
    sc.fill(BLACK)
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            for l in points:
                print("point(", l.x, ",", l.y, "),")
            exit()
        if i.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] == 1:
                tempMousePos = pygame.mouse.get_pos()
                points.append(point(tempMousePos[0], tempMousePos[1]))
        if i.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[K_SPACE]:
                points = []
    if len(points) != 0:
        delaun = delaunay(points, sc)
        graph = voronoi_graph(delaun.triangulate())
        voron_edge = graph.vg_build()
        for e in voron_edge:
            delaun.drawEdge(e)
        # print()
    pygame.display.update()
    clock.tick(FPS)
