import time
import math
import json
import random
from numbers import Real
from typing import Self

import pygame as pg

from ract.camera import Camera
from ract.hud import HUDElement
from ract.hud import HUD
from ract.menu import Menu
from ract.utils import EPSILON
from ract.utils import gen_tile_key
from ract.utils import gen_fnt_path
from ract.utils import gen_img_path
from data.weapons import SOUNDS
from data.weapons import WEAPONS
from data.levels import LEVELS
from data.levels import INDIVIDUALS

class Game(object):

    _SCREEN_SIZE = (960, 720)
    _SURF_RATIO = (3, 3)
    _SURF_SIZE = (
        int(_SCREEN_SIZE[0] / _SURF_RATIO[0]),
        int(_SCREEN_SIZE[1] / _SURF_RATIO[1]),
    )
    _SCREEN_FLAGS = pg.RESIZABLE | pg.SCALED
    _GAME_SPEED = 60

    def __init__(self: Self) -> None:
        pg.init()

        self._settings = {
            'graphics': {
                'vsync': 1,
                'multithreaded': 1,
                'fov': 90,
                'render_distance': 8,
            },
            'keys': {
                'interact': pg.K_e,
                'crouch': pg.K_LSHIFT,
                'slide': pg.K_LSHIFT,
                'jump': pg.K_SPACE,
                'forward': pg.K_w,
                'left': pg.K_a,
                'backward': pg.K_s,
                'right': pg.K_d,
                'look_left': pg.K_LEFT,
                'look_right': pg.K_RIGHT,
                'menu_up': pg.K_UP,
                'menu_down': pg.K_DOWN,
                'menu_enter': pg.K_RETURN,
                'pause': pg.K_ESCAPE, # not remappable
            },
        }
        self._screen = pg.display.set_mode(
            self._SCREEN_SIZE,
            flags=self._SCREEN_FLAGS,
            vsync=self._settings['graphics']['vsync']
        )
        pg.display.set_caption('Ract Demo')
        self._surface = pg.Surface(self._SURF_SIZE)
        self._running = 0
        
        # Level
        self._level = LEVELS[0]
        self._level.sounds = SOUNDS
        self._player = self._level.entities.player
        self._player.weapon = WEAPONS['shotgun']

        INDIVIDUALS['stalker'].state = 'stalking' 
        
        # Camera
        self._camera = Camera(
            fov=self._settings['graphics']['fov'],
            tile_size=self._SURF_SIZE[0] / 2,
            wall_render_distance=self._settings['graphics']['render_distance'],
            player=self._player,
            darkness=1,
            multithreaded=self._settings['graphics']['multithreaded'],
        )
        self._camera.horizon = 0.5
        self._camera.camera_offset = 5 / 6 * self._player.height
        self._camera.weapon_scale = 3 / self._SURF_RATIO[0]

        # Movement
        self._offset_ratio = 5 / 6
        self._player_height = 0.6
        self._crouch_height = 0.3125
        self._crouch_time = 10
        self._crouch_speed = 0.03
        self._crouch_friction = 0.7
        self._slide_height = 0.3125
        self._slide_time = 30
        self._slide_speed = 0.135
        self._slide_elevation_velocity = -0.075
        self._walk_speed = 0.0675
        self._walk_friction = 0.90625
        self._jump_velocity = 0.075
        self._key_look_speed = 2.5
        self._mouse_look_speed = 0.2

    def _update_crouch_height(self: Self, crouching: Real) -> None:
        self._player.height = self._player.try_height(
            pg.math.lerp(
                self._player_height,
                self._crouch_height,
                crouching / self._crouch_time,
            ),
        )

    def _get_crouching(self: Self, height: Real) -> Real:
        return pg.math.invlerp(
            self._player_height,
            self._crouch_height,
            height,
        ) * self._crouch_time

    def _update_slide_height(self: Self, sliding: Real) -> None:
        self._player.height = self._player.try_height(
            pg.math.lerp(
                self._slide_height,
                self._player_height,
                sliding / self._slide_time,
            ),
        )

    def _get_sliding(self: Self, height: Real) -> Real:
        return pg.math.invlerp(
            self._slide_height,
            self._player_height,
            height,
        ) * self._slide_time

    def run(self: Self) -> None:
        self._running = 1

        # Time
        start_time = time.time()
        level_timer = 0
        
        # Keys
        keys = pg.key.get_pressed()

        # Movement
        jumping = 0
        sliding = 0
        crouching = 0
        
        while self._running:
            # Time
            delta_time = time.time() - start_time
            start_time = time.time()
            rel_game_speed = delta_time * self._GAME_SPEED
            level_timer += rel_game_speed

            # Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self._running = 0
                if event.type == pg.MOUSEBUTTONDOWN:
                    self._player.attack()
                elif event.type == pg.KEYDOWN:
                    if event.key == self._settings['keys']['interact']:
                        self._player.interact()
                    elif not sliding:
                        if (event.key == self._settings['keys']['slide']
                            and jumping):
                            sliding = EPSILON
                            mult = (
                                keys[self._settings['keys']['forward']]
                                - keys[self._settings['keys']['backward']]
                            )
                            self._player.boost = (
                                self._player.forward
                                * self._slide_speed
                                * mult
                            )
                            self._player.elevation_velocity = (
                                self._slide_elevation_velocity
                            )
                        elif (event.key == self._settings['keys']['crouch']
                              and not jumping
                              and not crouching):
                            crouching = EPSILON
            
            # Keys
            keys = pg.key.get_pressed()
            
            # Hardcoded tile movement
            self._level.walls.set_tile(
                pos=(8, 11),
                elevation=math.sin(level_timer / 60 + math.pi) + 1,
            )
            self._level.walls.set_tile(
                pos=(9, 11),
                height=math.sin(level_timer / 60) + 1,
            )
            self._level.walls.set_tile(
                pos=(10, 8),
                elevation=0,
                height=2,
                texture=0,
                semitile={
                    'axis': 1,
                    'pos': (0.2, level_timer / 60 % 2 - 1),
                    'width': 1,
                },
                rect=(0.2, 0, 0.0001, 1),
            )
            
            # Movement
            speed = self._walk_speed
            self._player.friction = self._walk_friction

            # Slide / Crouch
            if sliding:
                sliding = min(sliding + rel_game_speed, self._slide_time)
                self._update_slide_height(sliding)
                sliding = self._get_sliding(self._player.height)
                if sliding >= self._slide_time:
                    sliding = 0
                    if not jumping:
                        crouching = EPSILON
            if crouching:
                if keys[self._settings['keys']['crouch']]:
                    crouching = min(
                        crouching + rel_game_speed, self._crouch_time,
                    )
                    speed = self._crouch_speed
                    self._player.friction = self._crouch_friction
                    self._update_crouch_height(crouching)
                else:
                    crouching = max(crouching - rel_game_speed, 0)
                    self._update_crouch_height(crouching)
                    crouching = self._get_crouching(self._player.height)
                    if not crouching:
                        self._player.height = self._player_height

            self._camera.camera_offset = (
                self._offset_ratio * self._player.height
            )
            
            movement = (
                (keys[self._settings['keys']['forward']]
                 - keys[self._settings['keys']['backward']])
                * speed, # FORWARD BACKWARD
                (keys[self._settings['keys']['right']]
                 - keys[self._settings['keys']['left']])
                * speed, # LEFT RIGHT
                (keys[self._settings['keys']['look_right']]
                 - keys[self._settings['keys']['look_left']])
                * self._key_look_speed, # LOOK LEFT RIGHT
                (keys[self._settings['keys']['jump']] and not jumping)
                * self._jump_velocity, # JUMP
            )
            self._player.update(
                rel_game_speed,
                level_timer,
                movement[0],
                movement[1],
                movement[2],
                movement[3] if movement[3] else None,
            )

            if keys[self._settings['keys']['jump']]:
                jumping = 1
            if self._player.collisions['e'][0]:
                jumping = 0

            self._level.update(rel_game_speed, level_timer)

            # Render
            self._camera.render(self._surface)
            # self._hud.render(self._surface)

            resized_surf = pg.transform.scale(self._surface, self._SCREEN_SIZE)
            self._screen.blit(resized_surf, (0, 0))
            pg.display.flip()
        
        pg.quit()

if __name__ == '__main__':
    Game().run()

