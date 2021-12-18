import numpy


# returns neighboring tiles going clockwise from north
# If outside boundaries, return the original tile
def neighbors(tile_map, x, y):

    N  = neighbor(tile_map, x, y, 0)
    NE = neighbor(tile_map, x, y, 1)
    E  = neighbor(tile_map, x, y, 2)
    SE = neighbor(tile_map, x, y, 3)
    S  = neighbor(tile_map, x, y, 4)
    SW = neighbor(tile_map, x, y, 5)
    W  = neighbor(tile_map, x, y, 6)
    NW = neighbor(tile_map, x, y, 7)

    if x < 0:
        NE = tile_map[x][y]
        E = tile_map[x][y]
        SE = tile_map[x][y]

    if y < 0:
        SE = tile_map[x][y]
        S = tile_map[x][y]
        SW = tile_map[x][y]

    if x > len(tile_map):
        NE = tile_map[x][y]
        E = tile_map[x][y]
        SE = tile_map[x][y]

    if y > len(tile_map[x]):
        NE = tile_map[x][y]
        N = tile_map[x][y]
        NW = tile_map[x][y]

    return N, NE, E, SE, S, SW, W, NW


def neighbor(tile_map, x, y, direction):
    #print(x, y, direction)
    #print(x + 1, len(tile_map) - 1, y + 1, len(tile_map[x]) - 1)

    #print((direction == 1) and (x + 1 > len(tile_map) - 1 or y + 1 > len(tile_map[x]) - 1))
    if (direction == 0 and y + 1 > len(tile_map[x]) - 1)\
            or ((direction == 1) and (x + 1 > len(tile_map) - 1 or y + 1 > len(tile_map[x]) - 1))\
            or (direction == 2 and x + 1 > len(tile_map) - 1)\
            or (direction == 3 and (x + 1 > len(tile_map) - 1 or y - 1 < 0))\
            or (direction == 4 and y - 1 < 0)\
            or (direction == 5 and (x - 1 < 0 or y - 1 < 0))\
            or (direction == 6 and x - 1 < 0)\
            or (direction == 7 and (x - 1 < 0 or y + 1 > len(tile_map[x]) - 1)):
        return tile_map[x][y]
    elif direction == 0:
        return tile_map[x][y + 1]
    elif direction == 1:
        return tile_map[x + 1][y + 1]
    elif direction == 2:
        return tile_map[x + 1][y]
    elif direction == 3:
        return tile_map[x + 1][y - 1]
    elif direction == 4:
        return tile_map[x][y - 1]
    elif direction == 5:
        return tile_map[x - 1][y - 1]
    elif direction == 6:
        return tile_map[x - 1][y]
    elif direction == 7:
        return tile_map[x - 1][y + 1]
    else:
        return tile_map[x][y]