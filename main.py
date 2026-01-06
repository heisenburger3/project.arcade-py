import arcade
from arcade.gui import UIManager, UILabel, UIFlatButton, UIBoxLayout, UIAnchorLayout
from level_1 import LevelFirst
from level_2 import LevelSecond
from level_3 import LevelThird
from level_4 import LevelFourth
from statistics import Statistics

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
                "font_size": 25,
                "font_name": "Times new roman"
            },
            "hover": {
                "font_color": arcade.color.Color(164, 114, 0, 255),
                "bg": arcade.color.Color(0, 0, 0, 100),
                "border": arcade.color.Color(164, 114, 0, 255),
                "border_width": 4,
                "font_size": 25,
                "font_name": "Times new roman"
            },
            "press": {
                "font_color": arcade.color.Color(145, 95, 0, 255),
                "bg": arcade.color.Color(0, 0, 0, 130),
                "border": arcade.color.Color(145, 95, 0, 255),
                "border_width": 4,
                "font_size": 25,
                "font_name": "Times new roman"
            },
            "disabled": {
                "font_color": arcade.color.DARK_GOLDENROD,
                "bg": arcade.color.Color(0, 0, 0, 70),
                "border": arcade.color.DARK_GOLDENROD,
                "border_width": 4,
                "font_size": 25,
                "font_name": "Times new roman"
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
                        align="center",
                        font_name="Times new roman")
        self.manager.add(title)

        anchor_layout = UIAnchorLayout()
        vert_layout = UIBoxLayout(vertical=True, space_between=50)

        hor_layout_1 = UIBoxLayout(vertical=False, space_between=200)
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

        hor_layout_2 = UIBoxLayout(vertical=False, space_between=200)
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

        stat_btn = UIFlatButton(text="Статистика",
                                width=400,
                                height=100,
                                x=self.width // 2 - 200,
                                y=self.height // 2 - 400,
                                style=self.btn_style)
        stat_btn.on_click = lambda event: self.stats()
        self.manager.add(stat_btn)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def first_level(self):
        self.manager.disable()
        level_view = LevelFirst(express=False)
        level_view.setup()
        self.window.show_view(level_view)

    def second_level(self):
        self.manager.disable()
        level_view = LevelSecond(express=False)
        level_view.setup(0)
        self.window.show_view(level_view)

    def third_level(self):
        self.manager.disable()
        level_view = LevelThird(express=False)
        level_view.setup(0)
        self.window.show_view(level_view)

    def fourth_level(self):
        self.manager.disable()
        level_view = LevelFourth(express=False)
        tile_map = arcade.load_tilemap('assets/fourth_level.tmx', scaling=TILE_SCALING)
        level_view.setup(0, tile_map, 0)
        self.window.show_view(level_view)

    def all_levels(self):
        self.manager.disable()
        level_view = LevelFirst()
        level_view.setup()
        self.window.show_view(level_view)

    def stats(self):
        self.manager.disable()
        stat_view = Statistics(self.btn_style)
        self.window.show_view(stat_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
