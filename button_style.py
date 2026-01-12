import arcade


class ButtonStyle:
    _instance = {
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

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ButtonStyle, cls).__new__(cls)
        return cls._instance
