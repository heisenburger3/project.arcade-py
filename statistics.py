import sqlite3
import arcade
from arcade.gui import UIManager, UITextArea, UILabel, UIFlatButton


def start():
    from main import StartView
    return StartView()


class Statistics(arcade.View):
    def __init__(self, style):
        super().__init__()
        arcade.set_background_color(arcade.color.Color(20, 0, 30, 255))
        self.style = style

        self.tab_style = {
            "normal": {
                "font_color": arcade.color.BLACK,
                "bg": arcade.color.Color(40, 191, 122, 255),
                "border": arcade.color.Color(0, 151, 82, 255),
                "border_width": 2,
                "font_size": 15,
                "font_name": "Times new roman"
            },
            "hover": {
                "font_color": arcade.color.BLACK,
                "bg": arcade.color.Color(40, 191, 122, 255),
                "border": arcade.color.Color(0, 151, 82, 255),
                "border_width": 2,
                "font_size": 15,
                "font_name": "Times new roman"
            },
            "press": {
                "font_color": arcade.color.BLACK,
                "bg": arcade.color.Color(40, 191, 122, 255),
                "border": arcade.color.Color(0, 151, 82, 255),
                "border_width": 2,
                "font_size": 15,
                "font_name": "Times new roman"
            },
            "disabled": {
                "font_color": arcade.color.BLACK,
                "bg": arcade.color.Color(40, 191, 122, 255),
                "border": arcade.color.Color(0, 151, 82, 255),
                "border_width": 2,
                "font_size": 15,
                "font_name": "Times new roman"
            },
        }
        self.click_tab_style = {
            "normal": {
                "font_color": arcade.color.BLACK,
                "bg": arcade.color.Color(0, 151, 82, 255),
                "font_size": 15,
                "font_name": "Times new roman"
            },
            "hover": {
                "font_color": arcade.color.BLACK,
                "bg": arcade.color.Color(0, 151, 82, 255),
                "font_size": 15,
                "font_name": "Times new roman"
            },
            "press": {
                "font_color": arcade.color.BLACK,
                "bg": arcade.color.Color(0, 151, 82, 255),
                "font_size": 15,
                "font_name": "Times new roman"
            },
            "disabled": {
                "font_color": arcade.color.BLACK,
                "bg": arcade.color.Color(0, 151, 82, 255),
                "font_size": 15,
                "font_name": "Times new roman"
            },
        }

        self.connection = sqlite3.Connection("assets/statistics.sqlite")
        self.cursor = self.connection.cursor()

        self.manager = UIManager()
        self.manager.enable()

        self.setup_widgets()

    def setup_widgets(self):
        self.texts = {"1 уровень": self.cursor.execute("select time from first_level order by time").fetchall(),
                      "2 уровень": self.cursor.execute("select time from second_level order by time").fetchall(),
                      "3 уровень": self.cursor.execute("select time from third_level order by time").fetchall(),
                      "4 уровень": self.cursor.execute("select time from fourth_level order by time").fetchall(),
                      "Все уровни": self.cursor.execute("select time from all_levels order by time").fetchall()}
        for key in self.texts.keys():
            for i in range(len(self.texts[key])):
                self.texts[key][i] = self.texts[key][i][0]

        title = UILabel(text="Статистика",
                        font_size=70,
                        text_color=arcade.color.DARK_KHAKI,
                        width=self.width,
                        x=0,
                        y=self.height - 150,
                        align="center",
                        font_name="Times new roman")
        self.manager.add(title)

        if self.texts["1 уровень"]:
            self.table = UITextArea(text="\n".join(list(map(lambda x: f"{x[0] + 1:3.0f}\t{' ' * 30}{x[1]:.2f}",
                                                            enumerate(self.texts["1 уровень"])))),
                                    font_size=25,
                                    text_color=arcade.color.LIGHT_GRAY,
                                    width=self.width - 400,
                                    height=350,
                                    x=200,
                                    y=self.height - 700,
                                    font_name="Times new roman")
        else:
            self.table = UITextArea(text=f"{' ' * 37}---",
                                    font_size=25,
                                    text_color=arcade.color.LIGHT_GRAY,
                                    width=self.width - 400,
                                    height=350,
                                    x=200,
                                    y=self.height - 700,
                                    font_name="Times new roman")
        self.manager.add(self.table)

        self.tab1 = UIFlatButton(x=188, y=660, width=125, height=70, text="1 уровень", style=self.click_tab_style)
        self.tab1.on_click = lambda event: self.new_table(self.tab1)
        self.manager.add(self.tab1)

        self.tab2 = UIFlatButton(x=313, y=660, width=125, height=70, text="2 уровень", style=self.tab_style)
        self.tab2.on_click = lambda event: self.new_table(self.tab2)
        self.manager.add(self.tab2)

        self.tab3 = UIFlatButton(x=438, y=660, width=125, height=70, text="3 уровень", style=self.tab_style)
        self.tab3.on_click = lambda event: self.new_table(self.tab3)
        self.manager.add(self.tab3)

        self.tab4 = UIFlatButton(x=563, y=660, width=125, height=70, text="4 уровень", style=self.tab_style)
        self.tab4.on_click = lambda event: self.new_table(self.tab4)
        self.manager.add(self.tab4)

        self.tab0 = UIFlatButton(x=688, y=660, width=124, height=70, text="Все уровни", style=self.tab_style)
        self.tab0.on_click = lambda event: self.new_table(self.tab0)
        self.manager.add(self.tab0)

        self.tabs = [self.tab1, self.tab2, self.tab3, self.tab4, self.tab0]
        self.clicked = self.tab1

        back_btn = UIFlatButton(text="Вернуться в меню",
                                x=self.width // 2 - 200,
                                y=self.height // 2 - 375,
                                width=400,
                                height=100,
                                style=self.style)
        back_btn.on_click = lambda event: self.come_back()
        self.manager.add(back_btn)

    def on_draw(self):
        self.clear()
        self.manager.draw()
        arcade.draw_rect_outline(arcade.XYWH(self.width // 2, self.height - 525, self.width - 380, 370),
                                 arcade.color.Color(0, 151, 82, 255), 4)
        arcade.draw_line(250, 660, 250, 290, arcade.color.Color(0, 151, 82, 255), 4)

    def new_table(self, sender):
        if sender is self.clicked:
            return None

        self.clicked.style = self.tab_style
        sender.style = self.click_tab_style
        self.clicked.hovered = True
        self.clicked.hovered = False
        self.clicked = sender

        self.manager.remove(self.table)
        if self.texts[sender.text]:
            self.table = UITextArea(text="\n".join(list(map(lambda x: f"{x[0] + 1:3.0f}\t{' ' * 30}{x[1]:.2f}",
                                                            enumerate(self.texts[sender.text])))),
                                    font_size=25,
                                    text_color=arcade.color.LIGHT_GRAY,
                                    width=self.width - 400,
                                    height=350,
                                    x=200,
                                    y=self.height - 700,
                                    font_name="Times new roman")
        else:
            self.table = UITextArea(text=f"{' ' * 37}---",
                                    font_size=25,
                                    text_color=arcade.color.LIGHT_GRAY,
                                    width=self.width - 400,
                                    height=350,
                                    x=200,
                                    y=self.height - 700,
                                    font_name="Times new roman")
        self.manager.add(self.table)

    def come_back(self):
        self.manager.disable()
        start_view = start()
        self.window.show_view(start_view)
