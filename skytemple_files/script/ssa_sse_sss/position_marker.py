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
from range_typed_integers import i16

from skytemple_files.common.util import AutoString, CheckedIntWrites
from skytemple_files.script.ssa_sse_sss.position import SsaPosition


class SsaPositionMarker(AutoString, CheckedIntWrites):
    pos: SsaPosition
    unk8: i16
    unkA: i16
    unkC: i16
    unkE: i16

    def __init__(self, pos: SsaPosition, unk8: i16, unkA: i16, unkC: i16, unkE: i16):
        self.pos = pos
        self.unk8 = unk8
        self.unkA = unkA
        self.unkC = unkC
        self.unkE = unkE
