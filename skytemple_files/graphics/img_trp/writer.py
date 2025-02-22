#  Copyright 2020-2022 Capypara and the SkyTemple Contributors
#
#  This file is part of SkyTemple.
#
#  SkyTemple is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SkyTemple is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SkyTemple.  If not, see <https://www.gnu.org/licenses/>.
from typing import Optional

from range_typed_integers import u32_checked

from skytemple_files.common.util import *
from skytemple_files.graphics.img_trp import PAL_LEN, PAL_ENTRY_LEN
from skytemple_files.graphics.img_trp.model import ImgTrp


class ImgTrpWriter:
    def __init__(self, model: ImgTrp):
        self.model = model

    def write(self) -> Tuple[bytes, List[int], Optional[int]]:
        buffer = bytearray()

        # Sprites
        spr_pointer = len(buffer)
        for tiles in self.model.sprites:
            for tile in tiles:
                buffer += tile

        # Palettes
        pal_pointer = len(buffer)
        data = bytearray(len(self.model.palettes) * PAL_LEN * PAL_ENTRY_LEN)
        cursor = 0
        for pal in self.model.palettes:
            for i, col in enumerate(pal):
                write_u8(data, u8(col), cursor)
                cursor += 1
                if i % 3 == 2:
                    write_u8(data, u8(0xAA), cursor)
                    cursor += 1
        buffer += data

        # Header
        header = bytearray(4*4)
        write_u32(header, u32_checked(spr_pointer), 0x00)
        write_u32(header, u32_checked(len(self.model.sprites)), 0x04)
        write_u32(header, u32_checked(pal_pointer), 0x08)
        write_u32(header, u32_checked(len(self.model.palettes) * PAL_LEN), 0x0C)
        pointer_offsets = [len(buffer), len(buffer) + 8]
        header_pointer = len(buffer)
        buffer += header

        return buffer, pointer_offsets, header_pointer
