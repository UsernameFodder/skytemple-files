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
# mypy: ignore-errors
import os

from ndspy.rom import NintendoDSRom

from skytemple_files.common.util import get_ppmdu_config_for_rom, get_binary_from_rom_ppmdu
from skytemple_files.hardcoded.default_starters import HardcodedDefaultStarters

base_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..')
rom_us = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy_us_unpatched.nds'))
rom_eu = NintendoDSRom.fromFile(os.path.join(base_dir, 'skyworkcopy.nds'))
ppmdu_us = get_ppmdu_config_for_rom(rom_us)
ppmdu_eu = get_ppmdu_config_for_rom(rom_eu)
arm9_us = get_binary_from_rom_ppmdu(rom_us, ppmdu_us.binaries['arm9.bin'])
arm9_eu = get_binary_from_rom_ppmdu(rom_eu, ppmdu_us.binaries['arm9.bin'])


def test(getter, setter, ov_us, ov_eu):
    assert getter(ov_us, ppmdu_us) == getter(ov_eu, ppmdu_eu)
    x = getter(ov_us, ppmdu_us)
    for e in x:
        print(e)
    x[0].poke_id = 999
    setter(x, ov_us, ppmdu_us)
    setter(x, ov_eu, ppmdu_eu)
    assert getter(ov_us, ppmdu_us) == x
    assert getter(ov_eu, ppmdu_eu) == x


test(
    HardcodedDefaultStarters.get_special_episode_pcs,
    HardcodedDefaultStarters.set_special_episode_pcs,
    arm9_us, arm9_eu
)
