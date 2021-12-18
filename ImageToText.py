import numpy
from PIL import Image

color_map = Image.open("res/terrain.png").convert('RGB')
color_map.load()
color_map = numpy.asarray(color_map)
color_map = color_map[:,:,:1].reshape(399, 540)
for y in range(540):
    for x in range(399):
        if color_map[x][y] == 52:
            color_map[x][y] = 0
        elif color_map[x][y] == 154:
            color_map[x][y] = 1
        elif color_map[x][y] == 229:
            color_map[x][y] = 2
        elif color_map[x][y] == 198:
            color_map[x][y] = 3
        else:
            color_map[x][y] = 9
print(color_map)
txt_file = open("test.txt", "w")
numpy.savetxt(txt_file, color_map, fmt="%d",delimiter="")

txt_file.close()
print(txt_file)
