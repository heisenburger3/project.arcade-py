import arcade


class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        """Так как центр текстур GreenWorm и GreenWorm_move в ресурсах arcade находится над видимой её частью, повороты 
        реализовывались некорректно из-за смещённых center_x и center_y, поэтому потребовалось добавить в assets 
        обрезанные до видимых частей картинки"""
        self.worm_texture = arcade.load_texture("assets/worm.png")
        self.texture = self.worm_texture
        self.move_texture = arcade.load_texture("assets/worm_move.png")
        self.scale = 0.38
        self.center_x = x
        self.center_y = y
        self.angle = 180

        self.textures = (self.texture, self.move_texture)
        self.current_texture = 0

    def move(self, change_x, change_y, transformation):
        angle = self.get_angle(change_x, change_y)
        if angle:
            self.angle = angle

        if change_x != 0 and change_y != 0:
            change_x /= 2 ** 0.5
            change_y /= 2 ** 0.5

        self.center_x += change_x
        self.center_y += change_y

        if transformation:
            self.current_texture = (self.current_texture + 1) % 2
            self.texture = self.textures[self.current_texture]

    def get_angle(self, change_x, change_y):
        if change_x == change_y == 0:
            return None
        elif change_x == 0:
            return 180 - 90 * change_y // abs(change_y)
        elif change_y == 0:
            return 90 + 90 * change_x // abs(change_x)
        elif change_y > 0:
            return 90 + 45 * change_x // abs(change_x)
        else:
            return 270 - 45 * change_x // abs(change_x)
