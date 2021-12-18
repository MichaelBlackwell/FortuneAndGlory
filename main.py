"""
Array Backed Grid Shown By Sprites

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.

This version makes a grid of sprites instead of numbers

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.array_backed_grid_sprites_2
"""
import PIL
import arcade
import networkx
import tcod

# The origin of the map
import numpy
from PIL import Image
from arcade import screen_to_isometric_grid, isometric_grid_to_screen
import timeit
import MapFunctions
from numpy import int32
import ProcGen
import MenuView



class MyGame(arcade.View):
    """
    Main application class.
    """

    # def neighbor_height_check




def main():

    window = arcade.Window(1920, 1080, "Different Views Minimal Example")
    menu_view = MenuView.MenuView()
    OverMapView = OverMapView.OverMapView()
    window.show_view(menu_view)
    arcade.run()



if __name__ == "__main__":
    main()
