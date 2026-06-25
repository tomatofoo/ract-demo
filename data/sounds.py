from pygame import mixer as mx

from ract.sound import patch_surround
from ract.sound import Sound
from ract.sound import SoundManager
from ract.utils import gen_sfx_path
from ract.utils import gen_mus_path


mx.init()
patch_surround()
SOUNDS = SoundManager(
    sounds={
        'shotgun': Sound(gen_sfx_path('shotgun.mp3')),
        'pickup': Sound(gen_sfx_path('pickup.mp3')),
        'water': Sound(gen_sfx_path('water.wav')),
    },
)

