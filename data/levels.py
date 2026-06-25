import math

import pygame as pg

from data.sounds import SOUNDS
from data.weapons import WEAPONS 
from ract.level import ColumnTexture
from ract.level import Walls
from ract.level import Floor
from ract.level import Sky 
from ract.level import Special
from ract.level import SpecialManager
from ract.level import Level
from ract.entities import Entity
from ract.entities import EntityExState
from ract.entities import EntityEx
from ract.entities import Stalker
from ract.entities import WeaponItem
from ract.entities import Player
from ract.entities import EntityManager
from ract.inventory import Collectible
from ract.inventory import Inventory
from ract.utils import gen_img_path
from ract.utils import gen_map_path


# LEVEL 0
textures = (
    (pg.image.load(gen_img_path('cacodemon', '1', '1.png')),
     pg.image.load(gen_img_path('cacodemon', '1', '2.png')),
     pg.image.load(gen_img_path('cacodemon', '1', '3.png')),
     pg.image.load(gen_img_path('cacodemon', '1', '4.png')),
     pg.image.load(gen_img_path('cacodemon', '1', '5.png')),
     pg.image.load(gen_img_path('cacodemon', '1', '6.png'))),
    (pg.image.load(gen_img_path('cacodemon', '2', '1.png')),
     pg.image.load(gen_img_path('cacodemon', '2', '2.png')),
     pg.image.load(gen_img_path('cacodemon', '2', '3.png')),
     pg.image.load(gen_img_path('cacodemon', '2', '4.png')),
     pg.image.load(gen_img_path('cacodemon', '2', '5.png')),
     pg.image.load(gen_img_path('cacodemon', '2', '6.png'))),
    (pg.image.load(gen_img_path('cacodemon', '3', '1.png')),
     pg.image.load(gen_img_path('cacodemon', '3', '2.png')),
     pg.image.load(gen_img_path('cacodemon', '3', '3.png')),
     pg.image.load(gen_img_path('cacodemon', '3', '4.png')),
     pg.image.load(gen_img_path('cacodemon', '3', '5.png')),
     pg.image.load(gen_img_path('cacodemon', '3', '6.png'))),
    (pg.image.load(gen_img_path('cacodemon', '4', '1.png')),
     pg.image.load(gen_img_path('cacodemon', '4', '2.png')),
     pg.image.load(gen_img_path('cacodemon', '4', '3.png')),
     pg.image.load(gen_img_path('cacodemon', '4', '4.png')),
     pg.image.load(gen_img_path('cacodemon', '4', '5.png')),
     pg.image.load(gen_img_path('cacodemon', '4', '6.png'))),
    (pg.image.load(gen_img_path('cacodemon', '5', '1.png')),
     pg.image.load(gen_img_path('cacodemon', '5', '2.png')),
     pg.image.load(gen_img_path('cacodemon', '5', '3.png')),
     pg.image.load(gen_img_path('cacodemon', '5', '4.png')),
     pg.image.load(gen_img_path('cacodemon', '5', '5.png')),
     pg.image.load(gen_img_path('cacodemon', '5', '6.png'))),
    (pg.image.load(gen_img_path('cacodemon', '6', '1.png')),
     pg.image.load(gen_img_path('cacodemon', '6', '2.png')),
     pg.image.load(gen_img_path('cacodemon', '6', '3.png')),
     pg.image.load(gen_img_path('cacodemon', '6', '4.png')),
     pg.image.load(gen_img_path('cacodemon', '6', '5.png')),
     pg.image.load(gen_img_path('cacodemon', '6', '6.png'))),
    (pg.image.load(gen_img_path('cacodemon', '7', '1.png')),
     pg.image.load(gen_img_path('cacodemon', '7', '2.png')),
     pg.image.load(gen_img_path('cacodemon', '7', '3.png')),
     pg.image.load(gen_img_path('cacodemon', '7', '4.png')),
     pg.image.load(gen_img_path('cacodemon', '7', '5.png')),
     pg.image.load(gen_img_path('cacodemon', '7', '6.png'))),
    (pg.image.load(gen_img_path('cacodemon', '8', '1.png')),
     pg.image.load(gen_img_path('cacodemon', '8', '2.png')),
     pg.image.load(gen_img_path('cacodemon', '8', '3.png')),
     pg.image.load(gen_img_path('cacodemon', '8', '4.png')),
     pg.image.load(gen_img_path('cacodemon', '8', '5.png')),
     pg.image.load(gen_img_path('cacodemon', '8', '6.png'))),
)
for animation in textures:
    for surf in animation:
        surf.set_colorkey((255, 0, 255))

TEST = EntityEx( # FOR PATHFINDING
    pos=(6.5, 0.5),
    elevation=1,
    width=0.4,
    height=0.6,
    climb=0.5,
    attack_width=0.4,
    render_width=0.6,
    states={'default': EntityExState(textures, 60)},
)

ENEMY = Stalker(
    pos=(8.5, 0.5),
    elevation=1,
    width=0.4,
    height=0.6,
    climb=0.5,
    attack_width=0.4,
    render_width=0.6,
    states={
        'default': EntityExState(textures, 60),
        'stalking': EntityExState(textures, 60),
    },
    gravity=0.004,
)

entities = {
    EntityEx(
        pos=(9, 9),
        elevation=3,
        width=0.5,
        height=0.75,
        attack_width=0.8,
        attack_height=0.8,
        render_width=1,
        render_height=1,
        states={'default': EntityExState(textures, 60)},
    ),
    Entity(
        pos=(9.5, 4.5),
        elevation=1,
        width=0.25,
        height=0.6,
        attack_width=0.4,
        render_width=1512 / 1486,
        render_height=1.0,
        textures=[
            pg.image.load(gen_img_path('speaker', '1.png')),
            pg.image.load(gen_img_path('speaker', '2.png')),
            pg.image.load(gen_img_path('speaker', '3.png')),
            pg.image.load(gen_img_path('speaker', '4.png')),
            pg.image.load(gen_img_path('speaker', '5.png')),
            pg.image.load(gen_img_path('speaker', '6.png')),
            pg.image.load(gen_img_path('speaker', '7.png')),
            pg.image.load(gen_img_path('speaker', '8.png')),
            pg.image.load(gen_img_path('speaker', '9.png')),
            pg.image.load(gen_img_path('speaker', '10.png')),
            pg.image.load(gen_img_path('speaker', '11.png')),
            pg.image.load(gen_img_path('speaker', '12.png')),
            pg.image.load(gen_img_path('speaker', '13.png')),
            pg.image.load(gen_img_path('speaker', '14.png')),
            pg.image.load(gen_img_path('speaker', '15.png')),
            pg.image.load(gen_img_path('speaker', '16.png')),
            pg.image.load(gen_img_path('speaker', '17.png')),
            pg.image.load(gen_img_path('speaker', '18.png')),
            pg.image.load(gen_img_path('speaker', '19.png')),
            pg.image.load(gen_img_path('speaker', '20.png')),
            pg.image.load(gen_img_path('speaker', '21.png')),
            pg.image.load(gen_img_path('speaker', '22.png')),
            pg.image.load(gen_img_path('speaker', '23.png')),
            pg.image.load(gen_img_path('speaker', '24.png')),
            pg.image.load(gen_img_path('speaker', '25.png')),
            pg.image.load(gen_img_path('speaker', '26.png')),
            pg.image.load(gen_img_path('speaker', '27.png')),
            pg.image.load(gen_img_path('speaker', '28.png')),
            pg.image.load(gen_img_path('speaker', '29.png')),
            pg.image.load(gen_img_path('speaker', '30.png')),
            pg.image.load(gen_img_path('speaker', '31.png')),
            pg.image.load(gen_img_path('speaker', '32.png')),
            pg.image.load(gen_img_path('speaker', '33.png')),
            pg.image.load(gen_img_path('speaker', '34.png')),
            pg.image.load(gen_img_path('speaker', '35.png')),
            pg.image.load(gen_img_path('speaker', '36.png')),
            pg.image.load(gen_img_path('speaker', '37.png')),
            pg.image.load(gen_img_path('speaker', '38.png')),
            pg.image.load(gen_img_path('speaker', '39.png')),
        ]
    ),
    Entity(
        pos=(6.5, 5),
        width=0.25,
        height=0.6,
        attack_width=0.4,
        render_width=0.5,
        textures=[pg.image.load(gen_img_path('GrenadeZombie.png'))],
    ),
    Entity(
        pos=(6.5, 4),
        width=0.25,
        height=0.6,
        attack_width=0.4,
        render_width=0.5,
        textures=[pg.image.load(gen_img_path('GrenadeZombie.png'))],
    ),
    Entity(
        pos=(6.5, 3),
        width=0.25,
        height=0.6,
        attack_width=0.4,
        render_width=0.5,
        textures=[pg.image.load(gen_img_path('GrenadeZombie.png'))],
    ),
    Entity(
        pos=(6.5, 2),
        width=0.25,
        height=0.6,
        attack_width=0.4,
        render_width=0.5,
        textures=[pg.image.load(gen_img_path('GrenadeZombie.png'))],
    ),
    TEST,
    ENEMY,
    WeaponItem(
        weapon=WEAPONS['shotgun'],
        number=5,
        pos=(7.5, 3),
        width=1,
        height=0.5,
        render_width=1,
        render_height=0.1875,
    ),
}
for dex, entity in enumerate(entities):
    entity.darkness = 0

player = Player(
    pos=(6.5, 7),
    inventory=Inventory(
        weapons={
            WEAPONS['fist']: math.inf,
            WEAPONS['shotgun']: 5,
            WEAPONS['launcher']: math.inf,
        }
    ),
)
player.yaw = 180
player.elevation = 1
entities = EntityManager(player, entities)
wall_textures = (
    ColumnTexture(pg.image.load(gen_img_path(
        'tilesets', 'main', 'stone', 'brick.png',
    ))),
    ColumnTexture(pg.image.load(gen_img_path(
        'tilesets', 'main', 'iron', 'bars.png',
    ))),
    ColumnTexture(pg.image.load(gen_img_path(
        'tilesets', 'main', 'iron', 'bars_broken.png',
    ))),
)
specials = SpecialManager()
LEVEL = Level(
    floor=Floor(pg.image.load(gen_img_path('tilesets', 'main', 'wood.png'))),
    ceiling=Sky(pg.image.load(gen_img_path('nightsky.png'))),
    walls=Walls.load(gen_map_path('demo2.json'), wall_textures),
    specials=specials,
    entities=entities,
    sounds=SOUNDS,
)

