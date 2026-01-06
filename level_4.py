from pyglet.graphics import Batch
import arcade
import sqlite3
from player import Player
from end_view import EndView

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Worm's Dinner"
TILE_SCALING = 3.15
TILE_SIZE = 16
CAMERA_LERP = 0.1
DEAD_ZONE_W = int(SCREEN_WIDTH * 0.3)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.4)


class LevelFourth(arcade.View):
    def __init__(self, sound=None, express=True):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)
        self.sound = sound

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

        self.connection = sqlite3.Connection("assets/statistics.sqlite")
        self.cursor = self.connection.cursor()

        self.express = express

    def setup(self, time, tile_map, level):
        """Настраиваем игру здесь. Вызывается при старте и при рестарте"""
        # Списки спрайтов, спрайт карты и игрок
        self.player_list = arcade.SpriteList()
        self.apple_list = arcade.SpriteList()

        if level == 0:
            self.player_sprite = Player(48, 50)
            self.world_width = SCREEN_WIDTH
            self.world_height = SCREEN_HEIGHT
        elif level == 1:
            self.player_sprite = Player(933, 930)
            self.world_width = SCREEN_WIDTH
            self.world_height = SCREEN_HEIGHT * 2
        else:
            self.player_sprite = Player(933, 1940)
            self.world_width = SCREEN_WIDTH * 2
            self.world_height = SCREEN_HEIGHT * 2
        self.player_list.append(self.player_sprite)

        if not self.sound:
            self.audio = arcade.load_sound('assets/game_music.mp3', False)
            self.sound = arcade.play_sound(self.audio, 1.0, 0, True)

        self.batch = Batch()
        self.total_time = time

        # Списки тайлов
        self.collision_list = tile_map.sprite_lists['collision']
        self.base_list = tile_map.sprite_lists['base']
        self.path_list = tile_map.sprite_lists['path']
        self.walls_list = tile_map.sprite_lists['walls']
        self.walls2_list = tile_map.sprite_lists['walls2']

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.collision_list)

        # Переход на следующий уровень с помощью яблока
        apple1 = arcade.Sprite("assets/apple_11.png", 0.2)
        apple1.center_x = 933
        apple1.center_y = 930

        apple2 = arcade.Sprite("assets/apple_11.png", 0.2)
        apple2.center_x = 933
        apple2.center_y = 1940

        apple3 = arcade.Sprite("assets/apple_11.png", 0.2)
        apple3.center_x = 1940
        apple3.center_y = 1940
        self.apple_list.extend((apple1, apple2, apple3)[level:])

        self.transform_timer = 0
        self.transformation = False

        self.level = level

        self.world_camera.position = (self.player_sprite.center_x, self.player_sprite.center_y)

    def on_draw(self):
        """Отрисовка экрана"""
        self.clear()

        # Отрисовка карты и камеры
        self.camera_shake.update_camera()
        self.world_camera.use()
        self.base_list.draw()
        self.path_list.draw()
        self.walls_list.draw()
        self.walls2_list.draw()
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
            apple_collect = arcade.load_sound("assets/apple_collect.mp3", False)
            arcade.play_sound(apple_collect, 5.0, 0, False)
            apple.remove_from_sprite_lists()

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
            self.height - 30,
            arcade.color.WHITE,
            16,
            batch=self.batch,
            font_name="Times new roman"
        )

        if len(self.apple_list) == 2 and self.level == 0:
            tile_map = arcade.load_tilemap('assets/fourth_level_2.tmx', scaling=TILE_SCALING)
            next_map = LevelFourth(self.sound, express=self.express)
            next_map.setup(self.total_time, tile_map, 1)
            self.window.show_view(next_map)
        elif len(self.apple_list) == 1 and self.level == 1:
            tile_map = arcade.load_tilemap('assets/fourth_level_3.tmx', scaling=TILE_SCALING)
            next_map = LevelFourth(self.sound, express=self.express)
            next_map.setup(self.total_time, tile_map, 2)
            self.window.show_view(next_map)
        elif len(self.apple_list) == 0 and self.level == 2 and self.express:
            arcade.stop_sound(self.sound)
            self.cursor.execute(f"insert into all_levels(time) values({self.total_time:.2f})")
            self.connection.commit()
            end = EndView(self.total_time, "Полное прохождение")
            self.window.show_view(end)
        elif len(self.apple_list) == 0 and self.level == 2:
            arcade.stop_sound(self.sound)
            self.cursor.execute(f"insert into fourth_level(time) values({self.total_time:.2f})")
            self.connection.commit()
            end = EndView(self.total_time, "4 уровень")
            self.window.show_view(end)

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.W):
            self.up_pressed = True
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = True
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.UP, arcade.key.W):
            self.up_pressed = False
        elif key in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = False
        elif key in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif key in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False
