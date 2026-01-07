from pyglet.graphics import Batch
import arcade
import sqlite3
import random
from level_3 import LevelThird
from player import Player
from end_view import EndView
from arcade.particles import FadeParticle, Emitter, EmitBurst

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Worm's Dinner"
TILE_SCALING = 3.15
TILE_SIZE = 16
CAMERA_LERP = 0.1
DEAD_ZONE_W = int(SCREEN_WIDTH * 0.3)
DEAD_ZONE_H = int(SCREEN_HEIGHT * 0.4)

SPARK_TEX = [
    arcade.make_soft_circle_texture(12, arcade.color.YELLOW),
    arcade.make_soft_circle_texture(12, arcade.color.PINK),
    arcade.make_soft_circle_texture(12, arcade.color.LIGHT_CYAN),
    arcade.make_soft_circle_texture(12, arcade.color.ELECTRIC_CRIMSON),
]


def gravity_drag(p):
    p.change_y += -0.03
    p.change_x *= 0.92
    p.change_y *= 0.92


def make_explosion(x, y, count=80):
    return Emitter(
        center_xy=(x, y),
        emit_controller=EmitBurst(count),
        particle_factory=lambda e: FadeParticle(
            filename_or_texture=random.choice(SPARK_TEX),
            change_xy=arcade.math.rand_in_circle((0.0, 0.0), 9.0),
            lifetime=random.uniform(0.5, 1.1),
            start_alpha=255, end_alpha=0,
            scale=random.uniform(0.35, 0.6),
            mutation_callback=gravity_drag,
        ),
    )


class LevelSecond(arcade.View):
    def __init__(self, sound=None, express=True):
        super().__init__()
        arcade.set_background_color(arcade.color.GRAY)
        self.sound = sound

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

        self.emitters = []

    def setup(self, time):
        """Настраиваем игру здесь. Вызывается при старте и при рестарте"""
        # Списки спрайтов, спрайт карты и игрок
        self.player_list = arcade.SpriteList()
        self.apple_list = arcade.SpriteList()
        tile_map = arcade.load_tilemap('assets/second_level.tmx', scaling=TILE_SCALING)
        self.player_sprite = Player(48, 50)
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

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, self.collision_list)

        # Переход на следующий уровень с помощью яблока
        apple = arcade.Sprite("assets/apple_11.png", 0.2)
        apple.center_x = 933
        apple.center_y = 930
        self.apple_list.append(apple)

        self.world_width = SCREEN_WIDTH

        self.world_height = SCREEN_HEIGHT

        self.time_stop = False
        self.stop_time = 0.0

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
        for e in self.emitters:
            e.draw()
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

        if not self.time_stop:
            self.total_time += delta_time
        else:
            self.stop_time += delta_time
        self.fonts = arcade.Text(
            f"Время: {self.total_time:.2f} сек",
            10,
            self.height - 30,
            arcade.color.WHITE,
            16,
            batch=self.batch,
            font_name="Times new roman"
        )

        emitters_copy = self.emitters.copy()
        for e in emitters_copy:
            e.update(delta_time)
        for e in emitters_copy:
            if e.can_reap():
                self.emitters.remove(e)

        if len(self.apple_list) == 0 and self.express:
            level_third = LevelThird(self.sound)
            level_third.setup(self.total_time)
            self.window.show_view(level_third)
        elif len(self.apple_list) == 0 and self.stop_time == 0:
            arcade.stop_sound(self.sound)
            self.cursor.execute(f"insert into second_level(time) values({self.total_time:.2f})")
            self.connection.commit()
            self.time_stop = True
            self.burst()
        elif len(self.apple_list) == 0 and self.stop_time >= 0.8:
            end = EndView(self.total_time, "2 уровень")
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

    def burst(self):
        self.emitters.append(make_explosion(933, 930))
