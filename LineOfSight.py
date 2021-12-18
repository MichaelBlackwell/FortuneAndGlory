'''
3DDDA
https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm


loop through all tiles
    set source and destination(tile)
    use brensenham to get a list of tiles between source and destination.
    loop through brensenham list
        use y=mx+b to determine if any tile is above this line
        if any return false


fog of war
    you can see a certain radius if clear minus any LOS blockage
    tell player general direction of the enemy (maybe enemy counter turned black)
'''
from math import sqrt

import bresenham
import numpy


def checkLOS(heightmap, x1, y1, x2, y2):
    # print("")
    # print("")
    # print("")
    VIEWER_HEIGHT = 0.2

    source = (x1, y1, heightmap[x1][y1] + VIEWER_HEIGHT)
    destination = (x2, y2, heightmap[x2][y2] + VIEWER_HEIGHT)
    vector = (destination[0] - source[0], destination[1] - source[1], destination[2] - source[2])
    distance = sqrt(vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2])
    l = list(bresenham.bresenham(x1, y1, x2, y2))
    # print("l")
    # print(l)
    if distance == 0:
        distance += 0.0001
    slope = vector[2] / distance

    # print("SLOPE")
    # print(slope)

    for p in l[1:]:
        dx = p[0] - source[0]
        dy = p[1] - source[1]
        distance2 = sqrt(dx * dx + dy * dy)
        # print("")
        # print("SLOPE")
        # print(slope)
        # print("")
        # print("distance2")
        # print(distance2)
        # print("")
        # print("p[0]][p[1]]")
        # print(heightmap[p[0]][p[1]])
        # print("")
        # print("slope * distance2 + heightmap[p] + VIEWER_HEIGHT")
        # print(slope * distance2 + heightmap[source[0]][source[1]] + VIEWER_HEIGHT)

        if heightmap[p[0]][p[1]] > slope * distance2 + heightmap[source[0]][source[1]] + VIEWER_HEIGHT:
            # print("")
            # print("NO")
            return False
    # print("")
    # print("YES")
    return True
