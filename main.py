from pyglet.graphics import Batch
import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Worm Dinner"
TILE_SCALING = 3.15
TILE_SIZE = 16
SPEED = 0
CAMERA_LERP = 0.1
# Мёртвая зона камеры
DEAD_ZONE_W = int(SCREEN_WIDTH * 0.3)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.4)


class StartView(arcade.View): # Главное меню игры
    def on_show(self):
        """Настройка начального экрана"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Отрисовка начального экрана"""
        self.clear()

        # Батч для текста
        self.batch = Batch()
        start_text = arcade.Text("Worm Dinner", self.window.width / 2, self.window.height / 2,
                                 arcade.color.WHITE, font_size=50, anchor_x="center", batch=self.batch)
        any_key_text = arcade.Text("Any key to start",
                                   self.window.width / 2, self.window.height / 2 - 75,
                                   arcade.color.GRAY, font_size=20, anchor_x="center", batch=self.batch)
        self.batch.draw()

    def on_key_press(self, key, modifiers):
        """Начало игры при нажатии клавиши"""
        level_view = LevelFirst()
        level_view.setup()
        self.window.show_view(level_view)


class LevelFirst(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)

        # Камеры: мир и GUI
        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.world_camera.view_data,
            max_amplitude=15.0,
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )

    def setup(self):
        """Настраиваем игру здесь. Вызывается при старте и при рестарте"""
        # Списки спрайтов, спрайт карты и игрок
        self.player_list = arcade.SpriteList()
        self.apple_list = arcade.SpriteList()
        tile_map = arcade.load_tilemap('assets/first_level.tmx', scaling=TILE_SCALING)
        self.player_sprite = arcade.Sprite(":resources:images/enemies/wormGreen.png",
                                           0.38)
        self.total_time = 0.0
        self.player_sprite.center_x = 48
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        self.batch = Batch()

        # Подсёт очков
        self.score = 0

        # С помощью этого, наш червяк сможет адекватно передвигаться с зажатыми клавишами
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        # Списки тайлов
        self.collision_list = tile_map.sprite_lists['collision']
        self.base_list = tile_map.sprite_lists['base']
        self.path_list = tile_map.sprite_lists['path']

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.collision_list)

        # Переход на следующий уровень с помощью яблока
        apple = arcade.Sprite("assets/apple_11.png", 0.2)
        apple.center_x = 933
        apple.center_y = 930
        self.apple_list.append(apple)

        self.world_width = SCREEN_WIDTH

        self.world_height = SCREEN_HEIGHT

    def on_draw(self):
        """Отрисовка экрана"""
        self.clear()

        # Отрисовка карты и камеры
        self.camera_shake.update_camera()
        self.world_camera.use()
        self.base_list.draw()
        self.path_list.draw()
        self.apple_list.draw()
        self.player_list.draw()
        self.gui_camera.use()
        self.camera_shake.readjust_camera()
        self.batch.draw()

    def on_update(self, delta_time: float):
        self.physics_engine.update()
        self.camera_shake.update(delta_time)
        apples_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.apple_list)

        for apple in apples_hit_list:
            self.camera_shake.start()
            self.score += 100
            apple.remove_from_sprite_lists()

        self.score_text = arcade.Text(
            f"Счет: {self.score}", 10, SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 20, batch=self.batch)

        # С помощью этого, наш червяк сможет адекватно передвигаться с зажатыми клавишами + расчёт скорости червяка
        # (одинаковая скорость при любом FPS)

        change_x = 0
        change_y = 0

        if self.up_pressed and not self.down_pressed:
            change_y = TILE_SIZE * TILE_SCALING * delta_time * 4
        elif self.down_pressed and not self.up_pressed:
            change_y = -(TILE_SIZE * TILE_SCALING * delta_time) * 4
        if self.left_pressed and not self.right_pressed:
            change_x = -(TILE_SIZE * TILE_SCALING * delta_time) * 4
        elif self.right_pressed and not self.left_pressed:
            change_x = TILE_SIZE * TILE_SCALING * delta_time * 4

        self.player_sprite.change_x = change_x
        self.player_sprite.change_y = change_y

        position = (
            self.player_sprite.center_x,
            self.player_sprite.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(  # Изменяем позицию камеры
            self.world_camera.position,
            position,
            CAMERA_LERP,
        )# Плавность следования камеры

        self.total_time += delta_time
        self.fonts = arcade.Text(
            f"Время: {self.total_time:.2f} сек",
            10,
            30,
            arcade.color.BLACK,
            16,
            batch=self.batch
        )

        if len(self.apple_list) == 0:
            level_second = LevelSecond()
            level_second.setup()
            self.window.show_view(level_second)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


class LevelSecond(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)

        # Камеры: мир и GUI
        self.world_camera = arcade.camera.Camera2D()
        self.gui_camera = arcade.camera.Camera2D()

        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.world_camera.view_data,
            max_amplitude=15.0,
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )

    def setup(self):
        """Настраиваем игру здесь. Вызывается при старте и при рестарте"""
        # Списки спрайтов, спрайт карты и игрок
        self.player_list = arcade.SpriteList()
        self.apple_list = arcade.SpriteList()
        tile_map = arcade.load_tilemap('assets/first_level.tmx', scaling=TILE_SCALING)
        self.player_sprite = arcade.Sprite(":resources:images/enemies/wormGreen.png",
                                           0.38)
        self.player_sprite.center_x = 48
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        self.batch = Batch()
        self.total_time = 0.0

        # Подсёт очков
        self.score = 100

        # Списки тайлов
        self.collision_list = tile_map.sprite_lists['collision']
        self.base_list = tile_map.sprite_lists['base']
        self.path_list = tile_map.sprite_lists['path']

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.collision_list)

        # Переход на следующий уровень с помощью яблока
        apple = arcade.Sprite("assets/apple_11.png", 0.2)
        apple.center_x = 933
        apple.center_y = 930
        self.apple_list.append(apple)

        self.world_width = SCREEN_WIDTH

        self.world_height = SCREEN_HEIGHT

    def on_draw(self):
        """Отрисовка экрана"""
        self.clear()

        # Отрисовка карты и камеры
        self.camera_shake.update_camera()
        self.world_camera.use()
        self.base_list.draw()
        self.path_list.draw()
        self.apple_list.draw()
        self.player_list.draw()
        self.gui_camera.use()
        self.camera_shake.readjust_camera()
        self.batch.draw()

    def on_update(self, delta_time: float):
        self.physics_engine.update()
        self.camera_shake.update(delta_time)
        apples_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.apple_list)

        for apple in apples_hit_list:
            self.camera_shake.start()
            self.score += 100
            apple.remove_from_sprite_lists()

        self.score_text = arcade.Text(
            f"Счет: {self.score}", 10, SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 20, batch=self.batch)

        change_x = 0
        change_y = 0

        if self.up_pressed and not self.down_pressed:
            change_y = TILE_SIZE * TILE_SCALING * delta_time * 4
        elif self.down_pressed and not self.up_pressed:
            change_y = -(TILE_SIZE * TILE_SCALING * delta_time) * 4
        if self.left_pressed and not self.right_pressed:
            change_x = -(TILE_SIZE * TILE_SCALING * delta_time) * 4
        elif self.right_pressed and not self.left_pressed:
            change_x = TILE_SIZE * TILE_SCALING * delta_time * 4

        # Устанавливаем изменение координат персонажа
        self.player_sprite.change_x = change_x
        self.player_sprite.change_y = change_y

        position = (
            self.player_sprite.center_x,
            self.player_sprite.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(  # Изменяем позицию камеры
            self.world_camera.position,
            position,
            CAMERA_LERP,
        )  # Плавность следования камеры

        self.total_time += delta_time
        self.fonts = arcade.Text(
            f"Время: {self.total_time:.2f} сек",
            10,
            30,
            arcade.color.BLACK,
            16,
            batch=self.batch
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False


def main():
    """Главная функция"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()