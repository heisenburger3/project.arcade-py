import arcade
import sqlite3
from arcade.gui import UIManager, UILabel, UIFlatButton
from button_style import ButtonStyle


def starting():
    from main import StartView
    return StartView()


class EndView(arcade.View):
    def __init__(self, time, level):
        super().__init__()
        arcade.set_background_color(arcade.color.Color(20, 0, 30, 255))
        self.time = float(f"{time:.2f}")
        self.level = level

        self.connection = sqlite3.Connection("assets/statistics.sqlite")
        self.cursor = self.connection.cursor()

        self.manager = UIManager()
        self.manager.enable()

        self.setup_widgets()

    def setup_widgets(self):
        title = UILabel(text=self.level,
                        font_size=75,
                        text_color=arcade.color.BLUE_GREEN,
                        width=self.width,
                        x=0,
                        y=self.height - 170,
                        align="center",
                        font_name="Times new roman")
        self.manager.add(title)

        result = UILabel(text=f"Ваш результат: {self.time:.2f}",
                         font_size=40,
                         text_color=arcade.color.WHITE,
                         width=self.width,
                         x=0,
                         y=self.height - 450,
                         align="center",
                         font_name="Times new roman")
        self.manager.add(result)

        self.stats = {"1 уровень": self.cursor.execute("select time from first_level order by time").fetchall(),
                      "2 уровень": self.cursor.execute("select time from second_level order by time").fetchall(),
                      "3 уровень": self.cursor.execute("select time from third_level order by time").fetchall(),
                      "4 уровень": self.cursor.execute("select time from fourth_level order by time").fetchall(),
                      "Все уровни": self.cursor.execute("select time from all_levels order by time").fetchall()}
        for key in self.stats.keys():
            for i in range(len(self.stats[key])):
                self.stats[key][i] = self.stats[key][i][0]

        if self.level[0] in '1234':
            top = self.stats[self.level].index(self.time) + 1
        else:
            top = self.stats["Все уровни"].index(self.time) + 1

        place = UILabel(text=f"Это топ-{top} среди всех результатов по данному уровню",
                        font_size=30,
                        text_color=arcade.color.COOL_GREY,
                        width=self.width,
                        x=0,
                        y=self.height - 500,
                        align="center",
                        font_name="Times new roman")
        self.manager.add(place)

        back_btn = UIFlatButton(text="Вернуться в меню",
                                x=self.width // 2 - 200,
                                y=self.height // 2 - 275,
                                width=400,
                                height=100,
                                style=ButtonStyle())
        back_btn.on_click = lambda event: self.start()
        self.manager.add(back_btn)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def start(self):
        self.manager.disable()
        start_view = starting()
        self.window.show_view(start_view)
