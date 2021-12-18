import numpy
import tcod


def find_river(heightmap, sizex, sizey):
    # gather 4 lists containing the tiles of all 4 edges
    edge1 = heightmap[0, :]
    edge2 = heightmap[sizex - 1, :]
    edge3 = heightmap[:, 0]
    edge4 = heightmap[:, sizey - 1]

    # find the lowest point on all 4 edges
    min_edge1 = numpy.argmin(edge1)
    min_edge2 = numpy.argmin(edge2)
    min_edge3 = numpy.argmin(edge3)
    min_edge4 = numpy.argmin(edge4)

    edge1loc = (0, min_edge1)
    edge2loc = (sizex - 1, min_edge2)
    edge3loc = (min_edge3, 0)
    edge4loc = (min_edge4, sizey - 1)

    # pathfind in all 6 combinations

    graph = tcod.path.SimpleGraph(cost=heightmap, cardinal=2, diagonal=0, greed=1)
    pathfinder1 = tcod.path.Pathfinder(graph)
    pathfinder2 = tcod.path.Pathfinder(graph)
    pathfinder3 = tcod.path.Pathfinder(graph)

    # pathfinder.add_root(edge1loc)
    # path1 = pathfinder.path_to(edge2loc).tolist()
    # print(path1)
    # pathfinder.clear()
    # pathfinder.add_root(edge1loc)
    # path2 = pathfinder.path_to(edge3loc).tolist()
    # print(path2)
    # pathfinder.clear()

    pathfinder1.add_root(edge1loc)
    # path2 = pathfinder.path_from(edge1loc)
    path3 = pathfinder1.path_to(edge4loc).tolist()
    pathfinder1.clear()
    # pathfinder.add_root(edge2loc)
    # path4 = pathfinder.path_to(edge3loc).tolist()
    # pathfinder.clear()
    pathfinder2.add_root(edge2loc)
    path5 = pathfinder2.path_to(edge4loc).tolist()
    pathfinder2.clear()
    pathfinder3.add_root(edge3loc)
    path6 = pathfinder3.path_to(edge4loc).tolist()
    pathfinder3.clear()

    # chose the path that is the flattest (differences in height)
    # flat1 = numpy.amax(heightmap[path1[0]][path1[1]], heightmap[path1[0]][path1[1]]) - numpy.amin(heightmap[path1[0]], heightmap[path1[1]])
    return path3, path5, path6


def find_forest(heightmap, sizex, sizey):
    # use a combination of height and noise
    forest = numpy.zeros((sizex, sizey))
    noise = tcod.noise.Noise(dimensions=2, algorithm=tcod.noise.Algorithm.SIMPLEX, seed=numpy.random.randint(0,10000))
    samples = noise[tcod.noise.grid(shape=(50, 50), scale=0.3, origin=(0, 0))]
    return (samples + 1.0).astype(int)

    # for x1 in range(sizex):
    #     for y1 in range(sizey):
    #         if perlin.perlin.two(p, x=x1, y=y1) > 3:
    #             forest[x1][y1] = 1
    # return forest
