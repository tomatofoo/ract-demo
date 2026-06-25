import math

import pygame as pg

from data.sounds import SOUNDS
from ract.utils import gen_img_path
from ract.entities import Missile
from ract.weapons import MeleeWeapon
from ract.weapons import HitscanWeapon
from ract.weapons import MissileWeapon

textures = {
    'shotgun': [
        pg.image.load(gen_img_path('shotgun', '1.png')),
        pg.image.load(gen_img_path('shotgun', '2.png')),
        pg.image.load(gen_img_path('shotgun', '3.png')),
        pg.image.load(gen_img_path('shotgun', '4.png')),
        pg.image.load(gen_img_path('shotgun', 'ground.png')),
    ],
}

for surfs in textures.values():
    for surf in surfs:
        surf.set_colorkey((255, 0, 255))


WEAPONS = {
    'shotgun': HitscanWeapon(
        damage=100,
        attack_range=20,
        cooldown=60,
        capacity=25,
        ground_textures=[
            textures['shotgun'][4],
        ],
        hold_textures=[textures['shotgun'][0]],
        attack_textures=[
            textures['shotgun'][1],
            textures['shotgun'][2],
            textures['shotgun'][3],
            textures['shotgun'][2],
            textures['shotgun'][1],
        ],
        ground_animation_time=1,
        hold_animation_time=30,
        attack_animation_time=50,
        # attack_sound=SOUNDS['shotgun'],
        # pickup_sound=SOUNDS['pickup'],
    ),
}

