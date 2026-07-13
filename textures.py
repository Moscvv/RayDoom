from settings import *
from enum import IntEnum, auto
from texture_id import *

TEX_PATH = 'assets/textures/'
#
WALL_TEX_PATH = TEX_PATH + 'walls/'
FLAT_TEX_PATH = TEX_PATH + 'flats/'


class Textures:
    def __init__(self):
        self.walls = self.get_textures(WALL_TEX_PATH, WallTexID)
        self.flats = self.get_textures(FLAT_TEX_PATH, FlatTexID)
        
    def get_textures(self, dir_path: str, texture_ids: IntEnum):
        textures = []
        for i in range(len(texture_ids)):
            texture = self.load_texture(dir_path + f'{i}.png', texture_ids)
            textures.append(texture)
        return textures  

    def load_texture(self, file_path, texture_ids):
        image = load_image(file_path)
        image_mipmaps(image)
        #
        texture = load_texture_from_image(image)
        set_texture_filter(texture, TEXTURE_FILTER_ANISOTROPIC_16X)
        unload_image(image)
        #
        return texture  

    def release(self):
        [unload_texture(tex) for tex in self.walls]
        [unload_texture(tex) for tex in self.ceils]
        [unload_texture(tex) for tex in self.floors]