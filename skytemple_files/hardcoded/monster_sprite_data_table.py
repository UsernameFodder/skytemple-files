"""
This table is stored in ARM9 and has two entries for every Pokémon base form.
- The first one seems to be how many 16x16 tile slots (or 256 byte pixels) the
  Pokémon's sprite will take up.
- The second is unknown, but also related to the sprite size?
"""
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
from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import *
from skytemple_files.common.i18n_util import f, _

ENTRY_LEN = 2


class MonsterSpriteDataTableEntry(AutoString, CheckedIntWrites):
    sprite_tile_slots: u8
    unk1: u8

    def __init__(self, sprite_tile_slots: u8, unk1: u8):
        self.sprite_tile_slots = sprite_tile_slots
        self.unk1 = unk1

    def to_bytes(self) -> bytes:
        return bytes([self.sprite_tile_slots, self.unk1])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MonsterSpriteDataTableEntry):
            return False
        return self.sprite_tile_slots == other.sprite_tile_slots and self.unk1 == other.unk1


class HardcodedMonsterSpriteDataTable:
    @classmethod
    def get(cls, arm9bin: bytes, config: Pmd2Data) -> List[MonsterSpriteDataTableEntry]:
        """Returns the list."""
        block = config.binaries['arm9.bin'].symbols['MonsterSpriteData']
        lst = []
        for i in range(block.begin, block.end, ENTRY_LEN):
            lst.append(MonsterSpriteDataTableEntry(
                read_u8(arm9bin, i + 0x00),
                read_u8(arm9bin, i + 0x01)
            ))
        return lst

    @classmethod
    def set(cls, value: List[MonsterSpriteDataTableEntry], arm9bin: bytearray, config: Pmd2Data) -> None:
        """
        Sets the list.
        The length of the list must exactly match the original ROM's length (see get).
        """
        block = config.binaries['arm9.bin'].symbols['MonsterSpriteData']
        expected_length = int((block.end - block.begin) / ENTRY_LEN)
        if len(value) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, entry in enumerate(value):
            arm9bin[block.begin + (i * ENTRY_LEN):block.begin + ((i + 1) * ENTRY_LEN)] = entry.to_bytes()


class IdleAnimType(Enum):
    STAND_LOOP = 0x00, _('Standing Animation (loop)')
    STAND_FRZ  = 0x01, _('Standing Animation (1st frame)')
    SPECIAL    = 0x02, _('Special')
    WALK_FRZ   = 0x03, _('Walking Animation (1st frame)')
    
    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(
            self, _: int, print_name: str
    ):
        self.print_name = print_name


class HardcodedMonsterGroundIdleAnimTable:
    @classmethod
    def get(cls, ov11bin: bytes, config: Pmd2Data) -> List[IdleAnimType]:
        """Returns the list."""
        block = config.binaries['overlay/overlay_0011.bin'].symbols['MonsterGroundIdleAnim']
        lst_i = list(ov11bin[block.begin:block.end])
        lst = [IdleAnimType(x) for x in lst_i]  # type: ignore
        return lst

    @classmethod
    def set(cls, values: List[IdleAnimType], ov11bin: bytearray, config: Pmd2Data) -> None:
        """
        Sets the list.
        The length of the list must exactly match the original ROM's length (see get).
        """
        block = config.binaries['overlay/overlay_0011.bin'].symbols['MonsterGroundIdleAnim']
        expected_length = block.end - block.begin
        if len(values) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        ov11bin[block.begin:block.end] = bytes([x.value for x in values])
