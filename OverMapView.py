import arcade
from pyglet.math import Vec2

import GameView


class OverMapView(arcade.View):

    def __init__(self):
        super().__init__()
        self.tile_map = None
        self.scene = None

        self.TILESIZE_X = 64
        self.TILESIZE_Y = 64

        self.camera_sprites = arcade.Camera(1920, 1080)

        arcade.set_background_color(arcade.color.BLACK)
        self.tile_map = arcade.tilemap.load_tilemap(map_file="OverWorld.json", scaling=0.25, use_spatial_hash=False)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

    def on_show(self):
        pass


    def on_draw(self):
        arcade.start_render()

        self.camera_sprites.use()

        self.scene.draw()


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # game_view.setup()
        # self.window.show_view(game_view)
        if _button == arcade.MOUSE_BUTTON_LEFT:
            self.camera_sprites.move(
                Vec2(self.camera_sprites.position[0] - arcade.get_window().width/2 + _x, self.camera_sprites.position[1] - arcade.get_window().height/2 + _y))

        if _button == arcade.MOUSE_BUTTON_RIGHT:
            game_view = GameView.GameView((int(self.camera_sprites.position[0] + _x) // self.TILESIZE_X),
                                          (int(self.camera_sprites.position[1] + _y) // self.TILESIZE_Y))
            # game_view.setup()
            self.window.show_view(game_view)



    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, _buttons: int, _modifiers: int):
        pass



