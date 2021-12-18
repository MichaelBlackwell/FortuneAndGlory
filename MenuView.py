import arcade

import GameView
import main
import OverMapView


class MenuView(arcade.View):
    """ Class that manages the 'menu' view. """

    def on_show(self):
        """ Called when switching to this view"""
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """ Draw the menu """
        arcade.start_render()
        arcade.draw_text("Menu Screen - click to advance", arcade.get_window().width / 2, arcade.get_window().height / 2,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ Use a mouse press to advance to the 'game' view. """
        next_view = GameView.GameView(0,50)
        # game_view.setup()
        self.window.show_view(next_view)



