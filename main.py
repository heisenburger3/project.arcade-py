from pyglet.graphics import Batch
import arcade
from level_1 import LevelFirst

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Worm's Dinner"
TILE_SCALING = 3.15
TILE_SIZE = 16
CAMERA_LERP = 0.1
DEAD_ZONE_W = int(SCREEN_WIDTH * 0.3)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.4)


class StartView(arcade.View):  # Главное меню игры
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        self.batch = Batch()
        start_text = arcade.Text("Worm's Dinner", self.window.width / 2, self.window.height / 2,
                                 arcade.color.WHITE, font_size=50, anchor_x="center", batch=self.batch)
        any_key_text = arcade.Text("Any key to start",
                                   self.window.width / 2, self.window.height / 2 - 75,
                                   arcade.color.GRAY, font_size=20, anchor_x="center", batch=self.batch)
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        level_view = LevelFirst()
        level_view.setup()
        self.window.show_view(level_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
