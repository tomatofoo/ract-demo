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


CACODEMON_TEXTURES = (
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
for i, animation in enumerate(CACODEMON_TEXTURES):
    for j, surf in enumerate(animation):
        surf.set_colorkey((255, 0, 255))

SHOTGUNNER_TEXTURES = (
    pg.image.load(gen_img_path('shotgunner', '1.png')),
    pg.image.load(gen_img_path('shotgunner', '2.png')),
    pg.image.load(gen_img_path('shotgunner', '3.png')),
    pg.image.load(gen_img_path('shotgunner', '4.png')),
    pg.image.load(gen_img_path('shotgunner', '5.png')),
    pg.image.load(gen_img_path('shotgunner', '6.png')),
    pg.image.load(gen_img_path('shotgunner', '7.png')),
    pg.image.load(gen_img_path('shotgunner', '8.png')),
)

INDIVIDUALS = {
    'stalker': Stalker(
        pos=(8.5, 0.5),
        elevation=1,
        width=0.4,
        height=0.6,
        climb=0.5,
        attack_width=0.4,
        render_width=0.6,
        states={
            'default': EntityExState(CACODEMON_TEXTURES, 60),
            'stalking': EntityExState(CACODEMON_TEXTURES, 60),
        },
        gravity=0.004,
    ),
}

entities = {
    Entity(
        pos=(6.5, 2.5),
        elevation=0,
        width=0.45,
        height=0.55,
        textures=SHOTGUNNER_TEXTURES,
    ),
    Entity(
        pos=(6.5, 3.5),
        elevation=0,
        width=0.45,
        height=0.55,
        textures=SHOTGUNNER_TEXTURES,
    ),
    Entity(
        pos=(6.5, 4.5),
        elevation=0,
        width=0.45,
        height=0.55,
        textures=SHOTGUNNER_TEXTURES,
    ),
    Entity(
        pos=(6.5, 5.5),
        elevation=0,
        width=0.45,
        height=0.55,
        textures=SHOTGUNNER_TEXTURES,
    ),
    EntityEx(
        pos=(9, 9),
        elevation=3,
        width=0.5,
        height=0.75,
        attack_width=0.8,
        attack_height=0.8,
        render_width=1,
        render_height=1,
        states={'default': EntityExState(CACODEMON_TEXTURES, 60)},
    ),
    *INDIVIDUALS.values(),
}
for dex, entity in enumerate(entities):
    entity.darkness = 0

player = Player(
    pos=(6.5, 7),
    inventory=Inventory(
        weapons={
            WEAPONS['shotgun']: math.inf,
        },
    ),
)
player.yaw = 180
player.elevation = 1
entities = EntityManager(player, entities)
wall_textures = (
    ColumnTexture(pg.image.load(gen_img_path('tiles', 'redbrick.png'))),
    ColumnTexture(pg.image.load(gen_img_path('tiles', 'bars.png'))),
    ColumnTexture(pg.image.load(gen_img_path('tiles', 'bars_broken.png'))),
)
specials = SpecialManager()
LEVELS = [
    Level(
        floor=Floor(pg.image.load(gen_img_path('tiles', 'wood.png'))),
        ceiling=Sky(pg.image.load(gen_img_path('sky.png'))),
        walls=Walls.load(gen_map_path('0.json'), wall_textures),
        specials=specials,
        entities=entities,
        sounds=SOUNDS,
    ),
]

