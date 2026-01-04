from pyglet.graphics import Batch
import arcade
from arcade.gui import UIManager, UILabel, UIFlatButton, UIBoxLayout, UIAnchorLayout
from level_1 import LevelFirst
from level_2 import LevelSecond
from level_3 import LevelThird
from level_4 import LevelFourth

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Worm's Dinner"
TILE_SCALING = 3.15
TILE_SIZE = 16
CAMERA_LERP = 0.1
DEAD_ZONE_W = int(SCREEN_WIDTH * 0.3)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.4)


class StartView(arcade.View):  # Главное меню игры
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.Color(20, 0, 30, 255))

        self.btn_style = {
            "normal": {
                "font_color": arcade.color.DARK_GOLDENROD,
                "bg": arcade.color.Color(0, 0, 0, 70),
                "border": arcade.color.DARK_GOLDENROD,
                "border_width": 4,
                "font_size": 25
            },
            "hover": {
                "font_color": arcade.color.Color(164, 114, 0, 255),
                "bg": arcade.color.Color(0, 0, 0, 100),
                "border": arcade.color.Color(164, 114, 0, 255),
                "border_width": 4,
                "font_size": 25
            },
            "press": {
                "font_color": arcade.color.Color(140, 90, 0, 255),
                "bg": arcade.color.Color(0, 0, 0, 130),
                "border": arcade.color.Color(140, 90, 0, 255),
                "border_width": 4,
                "font_size": 25
            },
            "disabled": {
                "font_color": arcade.color.DARK_GOLDENROD,
                "bg": arcade.color.Color(0, 0, 0, 70),
                "border": arcade.color.DARK_GOLDENROD,
                "border_width": 4,
                "font_size": 25
            },
        }

        self.manager = UIManager()
        self.manager.enable()

        self.setup_widgets()

    def setup_widgets(self):
        title = UILabel(text="Worm's Dinner",
                        font_size=85,
                        text_color=arcade.color.ARCADE_GREEN,
                        width=self.width,
                        x=0,
                        y=self.height - 200,
                        align="center")
        self.manager.add(title)

        anchor_layout = UIAnchorLayout()
        vert_layout = UIBoxLayout(vertical=True, space_between=50)

        hor_layout_1 = UIBoxLayout(vertical=False, space_between=250)
        lvl_1 = UIFlatButton(text="1 уровень",
                             width=300,
                             height=100,
                             style=self.btn_style)
        lvl_1.on_click = lambda event: self.first_level()
        hor_layout_1.add(lvl_1)
        lvl_2 = UIFlatButton(text="2 уровень",
                             width=300,
                             height=100,
                             style=self.btn_style)
        lvl_2.on_click = lambda event: self.second_level()
        hor_layout_1.add(lvl_2)
        vert_layout.add(hor_layout_1)

        hor_layout_2 = UIBoxLayout(vertical=False, space_between=250)
        lvl_3 = UIFlatButton(text="3 уровень",
                             width=300,
                             height=100,
                             style=self.btn_style)
        lvl_3.on_click = lambda event: self.third_level()
        hor_layout_2.add(lvl_3)
        lvl_4 = UIFlatButton(text="4 уровень",
                             width=300,
                             height=100,
                             style=self.btn_style)
        lvl_4.on_click = lambda event: self.fourth_level()
        hor_layout_2.add(lvl_4)
        vert_layout.add(hor_layout_2)

        all_lvls = UIFlatButton(text="Полное прохождение",
                                width=500,
                                height=100,
                                style=self.btn_style)
        all_lvls.on_click = lambda event: self.all_levels()
        vert_layout.add(all_lvls)

        anchor_layout.add(vert_layout)
        self.manager.add(anchor_layout)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def first_level(self):
        level_view = LevelFirst(express=False)
        level_view.setup()
        self.window.show_view(level_view)

    def second_level(self):
        level_view = LevelSecond(express=False)
        level_view.setup(0)
        self.window.show_view(level_view)

    def third_level(self):
        level_view = LevelThird(express=False)
        level_view.setup(0)
        self.window.show_view(level_view)

    def fourth_level(self):
        level_view = LevelFourth()
        tile_map = arcade.load_tilemap('assets/fourth_level.tmx', scaling=TILE_SCALING)
        level_view.setup(0, tile_map, 0)
        self.window.show_view(level_view)

    def all_levels(self):
        level_view = LevelFirst()
        level_view.setup()
        self.window.show_view(level_view)


class EndView(arcade.View):
    def __init__(self, time):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.time = time

    def on_draw(self):
        self.clear()
        self.batch = Batch()
        end_text = arcade.Text(f'Время: {self.time:.2f} сек', self.window.width / 2, self.window.height / 2,
                               arcade.color.WHITE, font_size=50, anchor_x="center", batch=self.batch)
        any_key_text = arcade.Text("R key to return to the start window",
                                   self.window.width / 2, self.window.height / 2 - 75,
                                   arcade.color.GRAY, font_size=20, anchor_x="center", batch=self.batch)
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            start_view = StartView()
            self.window.show_view(start_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
