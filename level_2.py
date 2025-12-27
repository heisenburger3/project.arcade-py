from pyglet.graphics import Batch
import arcade
from level_3 import LevelThird
from player import Player

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Worm's Dinner"
TILE_SCALING = 3.15
TILE_SIZE = 16
CAMERA_LERP = 0.1
DEAD_ZONE_W = int(SCREEN_WIDTH * 0.3)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.4)


class LevelSecond(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)

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
        tile_map = arcade.load_tilemap('assets/second_level.tmx', scaling=TILE_SCALING)
        self.player_sprite = Player(48, 50)
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

        self.transform_timer = 0
        self.transformation = False

    def on_draw(self):
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
            apple_collect = arcade.load_sound("assets/apple_collect.mp3", False)
            arcade.play_sound(apple_collect, 5.0, 0, False)
            apple.remove_from_sprite_lists()

        self.score_text = arcade.Text(
            f"Счет: {self.score}", 10, SCREEN_HEIGHT - 30,
            arcade.color.WHITE, 20, batch=self.batch)

        self.transform_timer += delta_time
        if self.transform_timer > 0.18:
            self.transformation = True
            self.transform_timer = 0

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

        if change_x != 0 or change_y != 0:
            self.player_sprite.move(change_x, change_y, self.transformation)
        self.transformation = False

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

        if len(self.apple_list) == 0:
            level_third = LevelThird()
            level_third.setup()
            self.window.show_view(level_third)

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
