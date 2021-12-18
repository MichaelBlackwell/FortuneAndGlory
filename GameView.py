import timeit

import arcade
import arcade.gui
import numpy
import PIL

import GameOverView
import ProcGen
import main
from LineOfSight import checkLOS

PIL.Image.MAX_IMAGE_PIXELS = None


ORIGIN = (40, 47)

# Set how many rows and columns we will have
ROW_COUNT = 50
COLUMN_COUNT = 50

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 40
HEIGHT = 20

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN = 5

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN_TITLE = "Array Backed Grid Buffered Example"

# --- Variables for our statistics

# Time for on_update
processing_time = 0

# Time for on_draw
draw_time = 0

global frame_count
global fps_start_timer
global fps
frame_count = 0
fps_start_timer = None
fps = None

def slice_sat_map(x,y):

    coordx = x * 50
    coordy = y * 50

    sat_map = PIL.Image.open("res/SatMap.png").convert('RGB')
    sat_map.load()
    sat_map = numpy.asarray(sat_map)
    sat_map = sat_map[coordy:coordy+50, coordx:coordx+50, :1]
    sat_map = sat_map.reshape(50, 50)
    return sat_map


class GameView(arcade.View):
    """ Manage the 'game' view for our program. """

    def __init__(self, satx, saty):
        """
        Set up the application.

        x: x position of tile of zoom in from sat map
        y: y position of tile of zomm in from sat map
        """
        super().__init__()

        # Slice of the Satellite heightmap
        self.height_map = None

        print("X")
        print(satx)
        print("Y")
        print(saty)

        self.satx = satx
        self.saty = saty

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()

        self.manager.enable()

        # Create a vertical BoxGroup for Left Side
        self.left_v_box = arcade.gui.UIBoxLayout(x=10, y=150, vertical=True)
        # Create an Enemy button
        enemy = arcade.gui.UIFlatButton(text="Enemy 1", width=200)
        self.left_v_box.add(enemy.with_space_around(bottom=20))
        # Create a Minimap
        texture = arcade.load_texture("res/diamond-shape001.png")
        minimap = arcade.gui.UITextureButton(texture=texture)
        self.left_v_box.add(minimap.with_space_around(bottom=20))

        # Create a vertical BoxGroup for Right Side
        self.right_v_box = arcade.gui.UIBoxLayout(x=10, y=150, vertical=True)
        # Create an Ally button
        ally = arcade.gui.UIFlatButton(text="Ally 1", width=200)
        self.right_v_box.add(ally.with_space_around(bottom=20))
        # Create an Stats button
        enemy = arcade.gui.UIFlatButton(text="Stats", width=200, height=200)
        self.right_v_box.add(enemy.with_space_around(bottom=20))

        # Create a horizontal BoxGroup for Bottom Side
        self.bottom_h_box = arcade.gui.UIBoxLayout(x=10, y=150, vertical=False)
        # Create an Ally button
        action1 = arcade.gui.UIFlatButton(text="action1", width=50, height=50)
        self.bottom_h_box.add(action1.with_space_around(bottom=20))
        # Create an Ally button
        action2 = arcade.gui.UIFlatButton(text="action2", width=50, height=50)
        self.bottom_h_box.add(action2.with_space_around(bottom=20))
        # Create an Ally button
        action3 = arcade.gui.UIFlatButton(text="action3", width=50, height=50)
        self.bottom_h_box.add(action3.with_space_around(bottom=20))

        # Create a horizontal BoxGroup for Top Side
        self.top_h_box = arcade.gui.UIBoxLayout(x=10, y=150, vertical=False)
        # Create an Ally button
        time_button = arcade.gui.UIFlatButton(text="time_button", width=100)
        self.top_h_box.add(time_button.with_space_around(bottom=20))









        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="bottom",
                child=self.left_v_box)
        )
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                anchor_y="bottom",
                child=self.right_v_box)
        )
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center",
                anchor_y="top",
                child=self.top_h_box)
        )
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center",
                anchor_y="bottom",
                child=self.bottom_h_box)
        )







        arcade.set_background_color(arcade.color.BLACK)

        # One dimensional list of all sprites in the two-dimensional sprite list
        self.grid_sprite_list = arcade.SpriteList()

        # This will be a two-dimensional grid of sprites to mirror the two
        # dimensional grid of numbers. This points to the SAME sprites that are
        # in grid_sprite_list, just in a 2d manner.
        self.grid_sprites = []
        self.normalized_heightmap = []
        self.hovered_tile = (0, 0)
        self.hovered_color = arcade.color.RED
        self.i = 0

        self.height_map = slice_sat_map(self.satx, self.saty)

        self.height_map = numpy.rot90(numpy.fliplr(self.height_map))

        # get map tile differences down to 1 incriments
        min = numpy.amin(self.height_map)
        max = numpy.amax(self.height_map)

        for x in range(len(self.height_map)):
            for y in range(len(self.height_map[x])):
                new_height = int((self.height_map[x][y] - min) // 4)
                self.height_map[x][y] = new_height + 1

        min = numpy.amin(self.height_map)
        max = numpy.amax(self.height_map)
        # Variables used to calculate frames per second

        # tiles containing a river
        river_tiles1, river_tiles2, river_tiles3 = ProcGen.find_river(self.height_map, ROW_COUNT, COLUMN_COUNT)

        # load sprite sheet
        flat_sprite = arcade.Sprite("res/Kenny Tiles/landscapeTiles_067.png", scale=1 / 33)

        #create forest map
        forest = ProcGen.find_forest(self.height_map, COLUMN_COUNT, ROW_COUNT)

        # Create a list of solid-color sprites to represent each grid location
        for row in range(ROW_COUNT):
            self.grid_sprites.append([])
            self.normalized_heightmap.append([])
            for column in range(COLUMN_COUNT):
                coord = arcade.isometric_grid_to_screen(row, column, ORIGIN[0], ORIGIN[1], WIDTH, HEIGHT)
                height_offset = self.height_map[row][column]

                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN)

                # choose which sprite to use
                # offset for taller sprites

                if [row, column] in river_tiles1 or [row, column] in river_tiles2 or [row, column] in river_tiles3:
                    sprite = arcade.Sprite("res/water.png", scale=1 / 3.3)
                    sprite.center_y = coord[1] + height_offset * 5
                elif forest[row][column] == 2:
                    sprite = arcade.Sprite("res/Forest.png", scale=1 / 3.3)
                    sprite.center_y = coord[1] + height_offset * 5
                else:
                    sprite = arcade.Sprite("res/Kenny Tiles/landscapeTiles_067.png", scale=1 / 3.3)
                    sprite.center_y = coord[1] + height_offset * 5
                sprite.center_x = coord[0]
                normalize = (self.height_map[row][column] - min + 10) / (max - min + 10)
                tint_height = int(255 * normalize)
                sprite.color = tint_height, tint_height, tint_height

                self.grid_sprite_list.append(sprite)
                self.grid_sprites[row].append(sprite)

        self.camera_sprites = arcade.Camera(arcade.get_window().width, arcade.get_window().height)
        self.camera_gui = arcade.Camera(arcade.get_window().width, arcade.get_window().height)

    def on_draw(self):
        """
        Render the screen.
        """

        # Start timing how long this takes

        start_time = timeit.default_timer()

        # --- Calculate FPS
        global frame_count
        global fps_start_timer
        global fps

        fps_calculation_freq = 60

        # Once every 60 frames, calculate our FPS
        if frame_count % fps_calculation_freq == 0:

            # Do we have a start time?
            if fps_start_timer is not None:
                # Calculate FPS
                total_time = timeit.default_timer() - fps_start_timer
                fps = fps_calculation_freq / total_time

            # Reset the timer
            fps_start_timer = timeit.default_timer()

        # Add one to our frame count
        frame_count += 1
        # print(fps)

        # This command has to happen before we start drawing
        arcade.start_render()

        # use sprite camera before drawing sprites
        self.camera_sprites.use()
        self.grid_sprite_list.draw()

        self.manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            selected = arcade.screen_to_isometric_grid(x, y - self.height_map[self.hovered_tile[0]][self.hovered_tile[1]] * 5, ORIGIN[0], ORIGIN[1], WIDTH, HEIGHT)

            print("Click coordinates: ({x}, {y}). Grid coordinates: ({selected[0]}, {selected[1]}). Height: ({self.height_map[selected[0]][selected[1]]}")
            # checkLOS(self.height_map, 9, 46, selected[0], selected[1])

            for x1 in range(COLUMN_COUNT):
                for y1 in range(ROW_COUNT):
                    if checkLOS(self.height_map,selected[0],selected[1],x1,y1):

                        self.grid_sprites[x1][y1].color = arcade.color.LIGHT_GRAY
                    else:
                        self.grid_sprites[x1][y1].color = arcade.color.CHARCOAL
            print(self.height_map)
            # Make sure we are on-grid. It is possible to click in the upper right
            # corner in the margin and go to a grid location that doesn't exist
            if selected[1] < ROW_COUNT and selected[0] < COLUMN_COUNT:

                # Flip the location between 1 and 0.
                if self.grid_sprites[selected[0]][selected[1]].color == arcade.color.WHITE:
                    self.grid_sprites[selected[0]][selected[1]].color = arcade.color.GREEN
                else:
                    self.grid_sprites[selected[0]][selected[1]].color = arcade.color.WHITE

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):

        selected = arcade.screen_to_isometric_grid(x, y - self.height_map[self.hovered_tile[0]][self.hovered_tile[1]] * 5, ORIGIN[0], ORIGIN[1], WIDTH,HEIGHT)  #

        if selected[0] != self.hovered_tile[0] and selected[1] != self.hovered_tile[1]:
            selected_tile = self.grid_sprites[selected[0]][selected[1]]
            self.grid_sprites[self.hovered_tile[0]][self.hovered_tile[1]].color = self.hovered_color
            self.hovered_color = selected_tile.color
            selected_tile.color = arcade.color.RED

            print("selected")
            print(selected)
            self.hovered_tile = selected



    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        self.camera_sprites.zoom(change=scroll_x)

        # for s in self.grid_sprite_list:
        #     if s.collides_with_point([x,y]):
        #         s.color = arcade.color.RED

        # Make sure we are on-grid. It is possible to click in the upper right
        # corner in the margin and go to a grid location that doesn't exist
