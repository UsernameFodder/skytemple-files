"""Module for editing the recruitment tables."""
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
from typing import cast

from skytemple_files.common.ppmdu_config.data import Pmd2Data
from skytemple_files.common.util import *


class HardcodedRecruitmentTables:
    @classmethod
    def get_monster_species_list(cls, overlay11bin: bytes, config: Pmd2Data) -> List[u16]:
        """Returns the list of Pokémon species from the recruitment table."""
        return cast(List[u16], cls._get_generic(overlay11bin, config, 'RecruitmentTableSpecies', 2))

    @classmethod
    def set_monster_species_list(cls, value: List[u16], overlay11bin: bytearray, config: Pmd2Data) -> None:
        """
        Sets the recruitment species list.
        The length of the list must exactly match the original ROM's length (see get_monster_species_list).
        """
        cls._set_generic(overlay11bin, config, 'RecruitmentTableSpecies', 2, value)
        
    @classmethod
    def get_monster_levels_list(cls, overlay11bin: bytes, config: Pmd2Data) -> List[u16]:
        """Returns the list of Pokémon levels from the recruitment table."""
        return cast(List[u16], cls._get_generic(overlay11bin, config, 'RecruitmentTableLevels', 2))

    @classmethod
    def set_monster_levels_list(cls, value: List[u16], overlay11bin: bytearray, config: Pmd2Data) -> None:
        """
        Sets the recruitment levels list.
        The length of the list must exactly match the original ROM's length (see get_monster_levels_list).
        """
        cls._set_generic(overlay11bin, config, 'RecruitmentTableLevels', 2, value)
        
    @classmethod
    def get_monster_locations_list(cls, overlay11bin: bytes, config: Pmd2Data) -> List[u8]:
        """Returns the list of Pokémon locations from the recruitment table."""
        return cast(List[u8], cls._get_generic(overlay11bin, config, 'RecruitmentTableLocations', 1))

    @classmethod
    def set_monster_locations_list(cls, value: List[u8], overlay11bin: bytearray, config: Pmd2Data) -> None:
        """
        Sets the recruitment locations list.
        The length of the list must exactly match the original ROM's length (see get_monster_locations_list).
        """
        cls._set_generic(overlay11bin, config, 'RecruitmentTableLocations', 1, value)

    @staticmethod
    def _get_generic(ov11: bytes, config: Pmd2Data, block_name: str, bytelen: int) -> List[int]:
        block = config.binaries['overlay/overlay_0011.bin'].symbols[block_name]
        lst = []
        for i in range(block.begin, block.end, bytelen):
            lst.append(read_dynamic(ov11, i, length=bytelen, big_endian=False, signed=False))
        return lst
    
    @staticmethod
    def _set_generic(ov11: bytearray, config: Pmd2Data, block_name: str, bytelen: int, value: Sequence[int]) -> None:
        block = config.binaries['overlay/overlay_0011.bin'].symbols[block_name]
        expected_length = int((block.end - block.begin) / bytelen)
        if len(value) != expected_length:
            raise ValueError(f"The list must have exactly the length of {expected_length} entries.")
        for i, entry in enumerate(value):
            if bytelen == 1:
                write_u8(ov11, u8(entry), block.begin + i * bytelen)
            elif bytelen == 2:
                write_u16(ov11, u16(entry), block.begin + i * bytelen)
            else:
                raise ValueError("Unsupported byte length.")
