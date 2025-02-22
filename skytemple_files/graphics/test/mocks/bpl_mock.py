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


# Testing mock class
from typing import List

from skytemple_files.graphics.bpl.protocol import BplProtocol, BplAnimationSpecProtocol


SIMPLE_DUMMY_PALETTE = [[0, 0, 0, 60, 70, 30, 120, 140, 60, 180, 210, 90, 240, 24, 120, 44, 94, 150, 104, 164, 180, 164, 234, 210, 224, 48, 240, 28, 118, 14, 88, 188, 44, 148, 2, 74, 208, 72, 104, 12, 142, 134, 72, 212, 164, 132, 26, 194], [0, 0, 0, 60, 70, 30, 120, 140, 60, 180, 210, 90, 240, 24, 120, 44, 94, 150, 104, 164, 180, 164, 234, 210, 224, 48, 240, 28, 118, 14, 88, 188, 44, 148, 2, 74, 208, 72, 104, 12, 142, 134, 72, 212, 164, 132, 26, 194], [0, 0, 0, 60, 70, 30, 120, 140, 60, 180, 210, 90, 240, 24, 120, 44, 94, 150, 104, 164, 180, 164, 234, 210, 224, 48, 240, 28, 118, 14, 88, 188, 44, 148, 2, 74, 208, 72, 104, 12, 142, 134, 72, 212, 164, 132, 26, 194], [0, 0, 0, 60, 70, 30, 120, 140, 60, 180, 210, 90, 240, 24, 120, 44, 94, 150, 104, 164, 180, 164, 234, 210, 224, 48, 240, 28, 118, 14, 88, 188, 44, 148, 2, 74, 208, 72, 104, 12, 142, 134, 72, 212, 164, 132, 26, 194], [0, 0, 0, 60, 70, 30, 120, 140, 60, 180, 210, 90, 240, 24, 120, 44, 94, 150, 104, 164, 180, 164, 234, 210, 224, 48, 240, 28, 118, 14, 88, 188, 44, 148, 2, 74, 208, 72, 104, 12, 142, 134, 72, 212, 164, 132, 26, 194], [0, 0, 0, 60, 70, 30, 120, 140, 60, 180, 210, 90, 240, 24, 120, 44, 94, 150, 104, 164, 180, 164, 234, 210, 224, 48, 240, 28, 118, 14, 88, 188, 44, 148, 2, 74, 208, 72, 104, 12, 142, 134, 72, 212, 164, 132, 26, 194], [0, 0, 0, 60, 70, 30, 120, 140, 60, 180, 210, 90, 240, 24, 120, 44, 94, 150, 104, 164, 180, 164, 234, 210, 224, 48, 240, 28, 118, 14, 88, 188, 44, 148, 2, 74, 208, 72, 104, 12, 142, 134, 72, 212, 164, 132, 26, 194], [0, 0, 0, 60, 70, 30, 120, 140, 60, 180, 210, 90, 240, 24, 120, 44, 94, 150, 104, 164, 180, 164, 234, 210, 224, 48, 240, 28, 118, 14, 88, 188, 44, 148, 2, 74, 208, 72, 104, 12, 142, 134, 72, 212, 164, 132, 26, 194], [0, 0, 0, 60, 70, 30, 120, 140, 60, 180, 210, 90, 240, 24, 120, 44, 94, 150, 104, 164, 180, 164, 234, 210, 224, 48, 240, 28, 118, 14, 88, 188, 44, 148, 2, 74, 208, 72, 104, 12, 142, 134, 72, 212, 164, 132, 26, 194], [0, 0, 0, 60, 70, 30, 120, 140, 60, 180, 210, 90, 240, 24, 120, 44, 94, 150, 104, 164, 180, 164, 234, 210, 224, 48, 240, 28, 118, 14, 88, 188, 44, 148, 2, 74, 208, 72, 104, 12, 142, 134, 72, 212, 164, 132, 26, 194], [0, 0, 0, 60, 70, 30, 120, 140, 60, 180, 210, 90, 240, 24, 120, 44, 94, 150, 104, 164, 180, 164, 234, 210, 224, 48, 240, 28, 118, 14, 88, 188, 44, 148, 2, 74, 208, 72, 104, 12, 142, 134, 72, 212, 164, 132, 26, 194], [0, 0, 0, 60, 70, 30, 120, 140, 60, 180, 210, 90, 240, 24, 120, 44, 94, 150, 104, 164, 180, 164, 234, 210, 224, 48, 240, 28, 118, 14, 88, 188, 44, 148, 2, 74, 208, 72, 104, 12, 142, 134, 72, 212, 164, 132, 26, 194], [0, 0, 0, 60, 70, 30, 120, 140, 60, 180, 210, 90, 240, 24, 120, 44, 94, 150, 104, 164, 180, 164, 234, 210, 224, 48, 240, 28, 118, 14, 88, 188, 44, 148, 2, 74, 208, 72, 104, 12, 142, 134, 72, 212, 164, 132, 26, 194], [0, 0, 0, 60, 70, 30, 120, 140, 60, 180, 210, 90, 240, 24, 120, 44, 94, 150, 104, 164, 180, 164, 234, 210, 224, 48, 240, 28, 118, 14, 88, 188, 44, 148, 2, 74, 208, 72, 104, 12, 142, 134, 72, 212, 164, 132, 26, 194], [0, 0, 0, 60, 70, 30, 120, 140, 60, 180, 210, 90, 240, 24, 120, 44, 94, 150, 104, 164, 180, 164, 234, 210, 224, 48, 240, 28, 118, 14, 88, 188, 44, 148, 2, 74, 208, 72, 104, 12, 142, 134, 72, 212, 164, 132, 26, 194], [0, 0, 0, 60, 70, 30, 120, 140, 60, 180, 210, 90, 240, 24, 120, 44, 94, 150, 104, 164, 180, 164, 234, 210, 224, 48, 240, 28, 118, 14, 88, 188, 44, 148, 2, 74, 208, 72, 104, 12, 142, 134, 72, 212, 164, 132, 26, 194]]


class BplAnimationSpecMock(BplAnimationSpecProtocol):
    def __init__(self, duration_per_frame: int, number_of_frames: int):
        self._duration_per_frame = duration_per_frame
        self._number_of_frames = number_of_frames

    # Properties; because the mock only supports reading!
    @property
    def duration_per_frame(self) -> int:  # type: ignore
        return self._duration_per_frame

    @property
    def number_of_frames(self) -> int:  # type: ignore
        return self._number_of_frames


class BplMock(BplProtocol[BplAnimationSpecMock]):
    def __init__(self, data: bytes) -> None:
        self._writing_allowed = False
        self.stub_init_data = data
        self._number_palettes: int = 16
        self._has_palette_animation: bool = True
        self._palettes: List[List[int]] = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 165, 148, 132, 74, 66, 49, 189, 165, 148, 58, 49, 41, 115, 99, 82, 214, 189, 173, 132, 107, 74, 41, 33, 25, 148, 132, 115, 197, 156, 132, 132, 115, 99, 247, 230, 206, 0, 0, 0], [0, 0, 0, 90, 74, 66, 107, 90, 74, 74, 58, 49, 99, 82, 74, 148, 132, 115, 123, 107, 90, 206, 181, 165, 107, 90, 82, 99, 74, 49, 82, 66, 58, 115, 82, 58, 58, 49, 33, 123, 90, 66, 132, 99, 74, 115, 99, 90], [0, 0, 0, 173, 148, 132, 156, 132, 115, 189, 173, 156, 181, 140, 107, 99, 82, 66, 222, 197, 181, 66, 58, 49, 140, 99, 74, 181, 156, 140, 148, 132, 115, 165, 140, 123, 123, 107, 90, 148, 132, 123, 148, 115, 90, 165, 148, 132], [0, 0, 0, 66, 49, 41, 99, 82, 74, 82, 58, 41, 74, 66, 58, 74, 49, 33, 66, 58, 49, 90, 66, 49, 49, 41, 33, 132, 115, 107, 107, 82, 58, 82, 66, 49, 99, 74, 58, 115, 99, 82, 82, 74, 66, 58, 41, 25], [0, 0, 0, 189, 165, 148, 132, 107, 90, 197, 173, 156, 222, 206, 181, 173, 156, 132, 99, 82, 66, 156, 132, 115, 74, 58, 49, 189, 148, 115, 206, 181, 165, 197, 173, 148, 214, 189, 156, 189, 173, 148, 214, 181, 148, 197, 181, 165], [0, 0, 0, 49, 41, 33, 66, 58, 49, 41, 33, 33, 58, 49, 41, 107, 90, 82, 132, 115, 107, 66, 49, 41, 90, 74, 66, 82, 66, 49, 74, 66, 58, 58, 58, 49, 74, 58, 41, 99, 74, 58, 82, 74, 66, 90, 82, 66], [0, 0, 0, 99, 82, 74, 115, 99, 82, 189, 173, 148, 132, 115, 99, 82, 66, 58, 140, 123, 107, 58, 49, 41, 123, 107, 90, 123, 99, 74, 107, 82, 58, 90, 74, 66, 156, 140, 115, 99, 82, 66, 140, 107, 82, 214, 189, 173], [0, 0, 0, 214, 189, 173, 90, 74, 66, 222, 197, 173, 197, 173, 148, 255, 230, 206, 189, 148, 115, 206, 165, 132, 173, 156, 140, 214, 189, 156, 230, 206, 181, 222, 197, 181, 148, 132, 115, 214, 181, 148, 206, 181, 165, 214, 197, 181], [0, 0, 0, 148, 115, 82, 115, 82, 58, 165, 123, 99, 140, 99, 74, 99, 74, 49, 123, 90, 66, 173, 140, 123, 115, 82, 66, 132, 107, 82, 132, 99, 66, 140, 115, 90, 82, 58, 41, 123, 99, 82, 132, 90, 66, 123, 107, 90], [0, 0, 0, 33, 25, 25, 49, 41, 41, 25, 25, 16, 66, 58, 49, 41, 33, 25, 58, 49, 41, 41, 41, 33, 33, 33, 25, 41, 33, 33, 49, 41, 33, 82, 74, 66, 58, 58, 49, 74, 58, 41, 66, 49, 41, 25, 16, 16], [0, 0, 0, 156, 132, 115, 132, 115, 99, 165, 140, 123, 82, 66, 58, 148, 115, 82, 214, 189, 173, 181, 140, 107, 165, 123, 90, 148, 123, 107, 140, 123, 115, 132, 107, 90, 123, 90, 74, 132, 115, 107, 189, 156, 123, 181, 165, 148], [0, 0, 0, 197, 156, 123, 181, 140, 107, 214, 181, 148, 230, 206, 181, 173, 156, 132, 206, 165, 132, 197, 173, 148, 247, 222, 197, 148, 123, 107, 123, 99, 74, 181, 165, 140, 214, 189, 156, 222, 197, 181, 173, 148, 132, 181, 156, 140], [0, 0, 0, 132, 107, 90, 140, 123, 107, 222, 197, 173, 148, 132, 115, 90, 74, 66, 140, 123, 99, 132, 115, 107, 132, 115, 99, 115, 99, 82, 123, 107, 99, 189, 148, 123, 140, 115, 90, 115, 99, 90, 173, 156, 140, 156, 123, 99], [0, 0, 0, 255, 239, 214, 222, 206, 189, 247, 222, 197, 197, 173, 156, 214, 197, 181, 197, 181, 165, 206, 189, 173, 230, 206, 181, 222, 197, 181, 255, 239, 214, 189, 165, 148, 222, 197, 173, 255, 239, 214, 255, 239, 214, 247, 222, 197], [0, 0, 0, 255, 107, 123, 148, 255, 115, 123, 140, 255, 90, 107, 132, 255, 74, 90, 123, 255, 107, 115, 132, 255, 123, 156, 189, 255, 148, 165, 181, 255, 0, 0, 0, 0, 123, 156, 197, 255, 107, 140, 181, 255, 148, 181, 214, 255], [0, 0, 0, 255, 132, 156, 173, 255, 132, 165, 206, 255, 148, 173, 197, 255, 197, 222, 247, 255, 107, 123, 148, 255, 74, 99, 123, 255, 140, 165, 181, 255, 156, 189, 214, 255, 181, 197, 222, 255, 132, 148, 173, 255, 140, 156, 181, 255]]
        self._animation_specs: List[BplAnimationSpecMock] = [
            BplAnimationSpecMock(0, 0),
            BplAnimationSpecMock(0, 0),
            BplAnimationSpecMock(0, 0),
            BplAnimationSpecMock(0, 0),
            BplAnimationSpecMock(0, 0),
            BplAnimationSpecMock(0, 0),
            BplAnimationSpecMock(0, 0),
            BplAnimationSpecMock(0, 0),
            BplAnimationSpecMock(0, 0),
            BplAnimationSpecMock(20, 4),
            BplAnimationSpecMock(0, 0),
            BplAnimationSpecMock(0, 0),
            BplAnimationSpecMock(0, 0),
            BplAnimationSpecMock(0, 0),
            BplAnimationSpecMock(0, 0),
            BplAnimationSpecMock(0, 0)
        ]
        self._animation_palette: List[List[int]] = [[0, 181, 255, 0, 181, 255, 0, 181, 255, 0, 181, 255, 0, 181, 255, 0, 181, 255, 0, 181, 255, 0, 181, 255, 0, 181, 255, 0, 181, 255, 0, 181, 255, 0, 181, 255, 0, 181, 255, 0, 181, 255, 0, 181, 255], [36, 128, 166, 37, 129, 167, 37, 129, 167, 37, 129, 167, 37, 129, 167, 37, 129, 167, 37, 129, 167, 37, 129, 167, 37, 129, 167, 37, 129, 167, 37, 129, 167, 37, 129, 167, 37, 129, 167, 37, 129, 167, 37, 129, 167], [33, 81, 101, 34, 81, 101, 34, 81, 101, 34, 81, 101, 34, 81, 101, 34, 81, 101, 34, 81, 101, 34, 81, 101, 34, 81, 101, 34, 81, 101, 34, 81, 101, 34, 81, 101, 34, 81, 101, 34, 81, 101, 34, 81, 101], [19, 33, 39, 20, 32, 39, 20, 32, 39, 20, 32, 39, 20, 32, 39, 20, 32, 39, 20, 32, 39, 20, 32, 39, 20, 32, 39, 20, 32, 39, 20, 32, 39, 20, 32, 39, 20, 32, 39, 20, 32, 39, 20, 32, 39]]

    # Properties; because the mock only supports reading!
    @property
    def number_palettes(self) -> int:  # type: ignore
        return self._number_palettes

    @property
    def has_palette_animation(self) -> bool:  # type: ignore
        return self._has_palette_animation

    @property
    def palettes(self) -> List[List[int]]:  # type: ignore
        return self._palettes

    @property
    def animation_specs(self) -> List[BplAnimationSpecMock]:  # type: ignore
        return self._animation_specs

    @property
    def animation_palette(self) -> List[List[int]]:  # type: ignore
        return self._animation_palette

    def import_palettes(self, palettes: List[List[int]]) -> None:
        if self._writing_allowed:
            self._palettes = palettes
            self._number_palettes = len(palettes)
            return
        raise NotImplementedError("Not implemented on mock.")

    def apply_palette_animations(self, frame: int) -> List[List[int]]:
        # TODO: Actual mocking!
        # noinspection PyProtectedMember
        from skytemple_files.graphics.bpl._model import Bpl
        return Bpl.apply_palette_animations(self, frame)  # type: ignore

    def is_palette_affected_by_animation(self, pal_idx: int) -> bool:
        raise NotImplementedError("Not implemented on mock.")

    def get_real_palettes(self) -> List[List[int]]:
        raise NotImplementedError("Not implemented on mock.")

    def set_palettes(self, palettes: List[List[int]]) -> None:
        raise NotImplementedError("Not implemented on mock.")

    def mock__enable_writing(self):
        """Enables very limited writing support on the mock, only implemented for very specific test scenarios."""
        self._writing_allowed = True


def _generate_mock_data():
    """Generate mock data using the assumed working implementation."""
    from skytemple_files.common.types.file_types import FileType
    with open('../fixtures/MAP_BG/coco.bpl', 'rb') as f:
        bpl = FileType.BPL.deserialize(f.read())

    for animation_spec in bpl.animation_specs:
        print(f"BplAnimationSpecMock({animation_spec.duration_per_frame}, {animation_spec.number_of_frames})")

    print(f"self._number_palettes = {bpl.number_palettes}")
    print(f"self._has_palette_animation = {bpl.has_palette_animation}")
    print(f"self._palettes = {bpl.palettes}")
    print(f"self._animation_palette = {bpl.animation_palette}")


if __name__ == '__main__':
    _generate_mock_data()
