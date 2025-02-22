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
import typing

from skytemple_files.common.impl_cfg import env_use_native
from skytemple_files.graphics.bma.handler import BmaHandler
from skytemple_files.graphics.bma.protocol import BmaProtocol
from skytemple_files.graphics.test.mocks.bpa_mock import BpaMock
from skytemple_files.graphics.test.mocks.bpc_mock import BpcMock
from skytemple_files.graphics.test.mocks.bpl_mock import BplMock
from skytemple_files.test.case import SkyTempleFilesTestCase, fixpath, romtest


class BmaTestCase(SkyTempleFilesTestCase[BmaHandler, BmaProtocol[BpaMock, BpcMock, BplMock]]):
    handler = BmaHandler

    def setUp(self) -> None:
        self.single_layer = self._load_main_fixture(self._fix_path_single_layer())
        self.assertIsNotNone(self.single_layer)
        self.two_layers = self._load_main_fixture(self._fix_path_two_layers())
        self.assertIsNotNone(self.two_layers)
        # TODO: Whoops. This one actually has 2 layers. The second is empty though.
        self.single_layer_one_col = self._load_main_fixture(self._fix_path_single_layer_one_col())
        self.assertIsNotNone(self.single_layer_one_col)
        self.two_layers_one_col = self._load_main_fixture(self._fix_path_two_layers_one_col())
        self.assertIsNotNone(self.two_layers_one_col)
        self.two_layers_two_col = self._load_main_fixture(self._fix_path_two_layers_two_col())
        self.assertIsNotNone(self.two_layers_two_col)
        self.two_layers_two_col_data = self._load_main_fixture(self._fix_path_two_layers_two_col_data())
        self.assertIsNotNone(self.two_layers_two_col_data)
        self.two_layers_data = self._load_main_fixture(self._fix_path_two_layers_data())
        self.assertIsNotNone(self.two_layers_data)
        self.one_layer_two_col = self._load_main_fixture(self._fix_path_one_layer_two_col())
        self.assertIsNotNone(self.one_layer_two_col)

        self._bpc_mock: BpcMock = BpcMock(bytes(), 8, 8, mock__number_of_layers=2)
        self._bpc_single_layer_mock: BpcMock = BpcMock(bytes(), 8, 8, mock__number_of_layers=1)
        self._bpl_mock = BplMock(bytes())
        self._bpas = [None, BpaMock(bytes()), None, None, None, None, None, None]

    def test_to_pil_single_layer(self) -> None:
        self._test_single_layer_image(self.single_layer, self._bpc_single_layer_mock, "single_layer", 1)
        self._test_single_layer_image(self.two_layers, self._bpc_mock, "two_layers", 2)
        self._test_single_layer_image(self.single_layer_one_col, self._bpc_single_layer_mock, "single_layer_one_col", 1)
        self._test_single_layer_image(self.two_layers_one_col, self._bpc_mock, "two_layers_one_col", 2)
        self._test_single_layer_image(self.two_layers_two_col, self._bpc_mock, "two_layers_two_col", 2)
        self._test_single_layer_image(self.two_layers_two_col_data, self._bpc_mock, "two_layers_two_col_data", 2)
        self._test_single_layer_image(self.two_layers_data, self._bpc_mock, "two_layers_data", 2)
        self._test_single_layer_image(self.one_layer_two_col, self._bpc_single_layer_mock, "one_layer_two_col", 1)

    def _test_single_layer_image(self, model: BmaProtocol, bpc_mock: BpcMock, typ: str, layers: int):
        for layer in range(0, layers):
            img = model.to_pil_single_layer(bpc_mock, self._bpl_mock.palettes, self._bpas, layer)
            self.assertImagesEqual(
                self._fix_path_expected("to_pil_single_layer", f"{typ}/{layer}.png"), img
            )

    def test_to_pil(self) -> None:
        kwargs = {
            'include_collision': False,
            'include_unknown_data_block': False,
            'pal_ani': True,
            'single_frame': False
        }
        ttyp = "to_pil"
        self._test_both_layers_image(self.single_layer, self._bpc_single_layer_mock, ttyp, "single_layer", **kwargs)
        self._test_both_layers_image(self.two_layers, self._bpc_mock, ttyp, "two_layers", **kwargs)
        self._test_both_layers_image(self.single_layer_one_col, self._bpc_single_layer_mock, ttyp, "single_layer_one_col", **kwargs)
        self._test_both_layers_image(self.two_layers_one_col, self._bpc_mock, ttyp, "two_layers_one_col", **kwargs)
        self._test_both_layers_image(self.two_layers_two_col, self._bpc_mock, ttyp, "two_layers_two_col", **kwargs)
        self._test_both_layers_image(self.two_layers_two_col_data, self._bpc_mock, ttyp, "two_layers_two_col_data", **kwargs)
        self._test_both_layers_image(self.two_layers_data, self._bpc_mock, ttyp, "two_layers_data", **kwargs)
        self._test_both_layers_image(self.one_layer_two_col, self._bpc_single_layer_mock, ttyp, "one_layer_two_col", **kwargs)

    def test_to_pil_debug(self) -> None:
        # If this is the Rust implementation, drawing collision and unknown data is not supported.
        if env_use_native():
            self.skipTest("This test is only enabled when the Python implementation is tested.")
        kwargs = {
            'include_collision': True,
            'include_unknown_data_block': True,
            'pal_ani': False,
            'single_frame': False
        }
        ttyp = "to_pil_debug"
        self._test_both_layers_image(self.single_layer, self._bpc_single_layer_mock, ttyp, "single_layer", **kwargs)
        self._test_both_layers_image(self.two_layers, self._bpc_mock, ttyp, "two_layers", **kwargs)
        self._test_both_layers_image(self.single_layer_one_col, self._bpc_single_layer_mock, ttyp, "single_layer_one_col", **kwargs)
        self._test_both_layers_image(self.two_layers_one_col, self._bpc_mock, ttyp, "two_layers_one_col", **kwargs)
        self._test_both_layers_image(self.two_layers_two_col, self._bpc_mock, ttyp, "two_layers_two_col", **kwargs)
        self._test_both_layers_image(self.two_layers_two_col_data, self._bpc_mock, ttyp, "two_layers_two_col_data", **kwargs)
        self._test_both_layers_image(self.two_layers_data, self._bpc_mock, ttyp, "two_layers_data", **kwargs)
        self._test_both_layers_image(self.one_layer_two_col, self._bpc_single_layer_mock, ttyp, "one_layer_two_col", **kwargs)

    def test_to_pil_single_frame_no_pal_ani(self) -> None:
        kwargs = {
            'include_collision': False,
            'include_unknown_data_block': False,
            'pal_ani': False,
            'single_frame': True
        }
        ttyp = "to_pil_single_frame_no_pal_ani"
        self._test_both_layers_image(self.single_layer, self._bpc_single_layer_mock, ttyp, "single_layer", **kwargs)
        self._test_both_layers_image(self.two_layers, self._bpc_mock, ttyp, "two_layers", **kwargs)
        self._test_both_layers_image(self.single_layer_one_col, self._bpc_single_layer_mock, ttyp, "single_layer_one_col", **kwargs)
        self._test_both_layers_image(self.two_layers_one_col, self._bpc_mock, ttyp, "two_layers_one_col", **kwargs)
        self._test_both_layers_image(self.two_layers_two_col, self._bpc_mock, ttyp, "two_layers_two_col", **kwargs)
        self._test_both_layers_image(self.two_layers_two_col_data, self._bpc_mock, ttyp, "two_layers_two_col_data", **kwargs)
        self._test_both_layers_image(self.two_layers_data, self._bpc_mock, ttyp, "two_layers_data", **kwargs)
        self._test_both_layers_image(self.one_layer_two_col, self._bpc_single_layer_mock, ttyp, "one_layer_two_col", **kwargs)

    def _test_both_layers_image(self, model: BmaProtocol, bpc_mock: BpcMock, test_typ: str, typ: str,
                                *, include_collision: bool, include_unknown_data_block: bool, pal_ani: bool,
                                single_frame: bool):
        imgs = model.to_pil(bpc_mock, self._bpl_mock, self._bpas,
                            include_collision, include_unknown_data_block, pal_ani, single_frame)
        for i, img in enumerate(imgs):
            self.assertImagesEqual(
                self._fix_path_expected(test_typ, f"{typ}/{i}.png"), img
            )

    def test_from_pil(self) -> None:
        self._bpc_mock.mock__enable_writing()
        self._bpl_mock.mock__enable_writing()
        self.two_layers.from_pil(
            self._bpc_mock, self._bpl_mock,
            self._load_image(self._fix_path_layer_import_lower()),
            self._load_image(self._fix_path_layer_import_upper()),
        )

        # Confirm BPL and BPC changes
        self.assertEqual(1, self._bpc_mock.tile_variant_1_written_to)
        self.assertEqual(0, self._bpc_mock.tile_variant_2_written_to)
        self.assertEqual(1, self._bpc_mock.tilemaps_variant_1_written_to)
        self.assertEqual(0, self._bpc_mock.tilemaps_variant_2_written_to)
        self.assertEqual([[44, 151, 205, 176, 222, 58, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 176, 255, 157, 255, 255, 255, 136, 136, 136, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 0, 255, 222, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 18, 171, 86, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [250, 255, 0, 0, 22, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 255, 255, 255, 136, 136, 136, 176, 255, 157, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [224, 224, 224, 225, 225, 225, 226, 226, 226, 227, 227, 227, 228, 228, 228, 229, 229, 229, 230, 230, 230, 231, 231, 231, 232, 232, 232, 233, 233, 233, 234, 234, 234, 235, 235, 235, 236, 236, 236, 237, 237, 237, 238, 238, 238, 239, 239, 239], [240, 240, 240, 241, 241, 241, 242, 242, 242, 243, 243, 243, 244, 244, 244, 245, 245, 245, 246, 246, 246, 247, 247, 247, 248, 248, 248, 249, 249, 249, 250, 250, 250, 251, 251, 251, 252, 252, 252, 253, 253, 253, 254, 254, 254, 255, 255, 255]], self._bpl_mock.palettes)
        self.assertEqual([1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2], self.two_layers.layer0)
        self.assertEqual([1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1], self.two_layers.layer1)

        # Confirm output / BMA mappings
        # The tiles will be returned from the mock, so they won't match, they will be the unchanged
        # BPC tiles for this test! But that's ok. We confirmed the correct BPL and BPC changes above.
        self.assertImagesEqual(
            self._fix_path_expected("from_pil", "0.png"), self.two_layers.to_pil_single_layer(
                self._bpc_mock, self._bpl_mock.palettes, self._bpas, 0
            )
        )
        self.assertImagesEqual(
            self._fix_path_expected("from_pil", "1.png"), self.two_layers.to_pil_single_layer(
                self._bpc_mock, self._bpl_mock.palettes, self._bpas, 1
            )
        )
        reloaded = self._save_and_reload_main_fixture(self.two_layers)
        self.assertEqual(self.two_layers.layer0, reloaded.layer0)
        self.assertEqual(self.two_layers.layer1, reloaded.layer1)

    def test_from_pil_one_to_two_layers(self) -> None:
        self._bpc_single_layer_mock.mock__enable_writing()
        self._bpl_mock.mock__enable_writing()
        self.single_layer.from_pil(
            self._bpc_single_layer_mock, self._bpl_mock,
            self._load_image(self._fix_path_layer_import_lower()),
            self._load_image(self._fix_path_layer_import_upper()),
        )

        # Confirm BPL and BPC changes
        self.assertEqual(1, self._bpc_single_layer_mock.tile_variant_1_written_to)
        self.assertEqual(0, self._bpc_single_layer_mock.tile_variant_2_written_to)
        self.assertEqual(1, self._bpc_single_layer_mock.tilemaps_variant_1_written_to)
        self.assertEqual(0, self._bpc_single_layer_mock.tilemaps_variant_2_written_to)
        self.assertEqual([[44, 151, 205, 176, 222, 58, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 176, 255, 157, 255, 255, 255, 136, 136, 136, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 0, 255, 222, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 18, 171, 86, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [250, 255, 0, 0, 22, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 255, 255, 255, 136, 136, 136, 176, 255, 157, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [224, 224, 224, 225, 225, 225, 226, 226, 226, 227, 227, 227, 228, 228, 228, 229, 229, 229, 230, 230, 230, 231, 231, 231, 232, 232, 232, 233, 233, 233, 234, 234, 234, 235, 235, 235, 236, 236, 236, 237, 237, 237, 238, 238, 238, 239, 239, 239], [240, 240, 240, 241, 241, 241, 242, 242, 242, 243, 243, 243, 244, 244, 244, 245, 245, 245, 246, 246, 246, 247, 247, 247, 248, 248, 248, 249, 249, 249, 250, 250, 250, 251, 251, 251, 252, 252, 252, 253, 253, 253, 254, 254, 254, 255, 255, 255]], self._bpl_mock.palettes)

        # Confirm output / BMA mappings
        # The tiles will be returned from the mock, so they won't match, they will be the unchanged
        # BPC tiles for this test! But that's ok. We confirmed the correct BPL and BPC changes above.
        self.assertImagesEqual(
            self._fix_path_expected("from_pil", "0.png"), self.single_layer.to_pil_single_layer(
                self._bpc_single_layer_mock, self._bpl_mock.palettes, self._bpas, 0
            )
        )
        self.assertImagesEqual(
            self._fix_path_expected("from_pil", "1.png"), self.single_layer.to_pil_single_layer(
                self._bpc_single_layer_mock, self._bpl_mock.palettes, self._bpas, 1
            )
        )
        reloaded = self._save_and_reload_main_fixture(self.single_layer)
        self.assertEqual(self.single_layer.layer0, reloaded.layer0)
        self.assertEqual(self.single_layer.layer1, reloaded.layer1)

    def test_from_pil_two_to_one_layer(self) -> None:
        self._bpc_mock.mock__enable_writing()
        self._bpl_mock.mock__enable_writing()
        self.two_layers.from_pil(
            self._bpc_mock, self._bpl_mock,
            self._load_image(self._fix_path_layer_import_lower())
        )

        # Confirm BPL and BPC changes
        self.assertEqual(1, self._bpc_mock.tile_variant_1_written_to)
        self.assertEqual(None, self._bpc_mock.tile_variant_2_written_to)
        self.assertEqual(1, self._bpc_mock.tilemaps_variant_1_written_to)
        self.assertEqual(None, self._bpc_mock.tilemaps_variant_2_written_to)
        self.assertEqual([[44, 151, 205, 176, 222, 58, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 176, 255, 157, 255, 255, 255, 136, 136, 136, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 0, 255, 222, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 18, 171, 86, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [250, 255, 0, 0, 22, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 255, 255, 255, 136, 136, 136, 176, 255, 157, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [224, 224, 224, 225, 225, 225, 226, 226, 226, 227, 227, 227, 228, 228, 228, 229, 229, 229, 230, 230, 230, 231, 231, 231, 232, 232, 232, 233, 233, 233, 234, 234, 234, 235, 235, 235, 236, 236, 236, 237, 237, 237, 238, 238, 238, 239, 239, 239], [240, 240, 240, 241, 241, 241, 242, 242, 242, 243, 243, 243, 244, 244, 244, 245, 245, 245, 246, 246, 246, 247, 247, 247, 248, 248, 248, 249, 249, 249, 250, 250, 250, 251, 251, 251, 252, 252, 252, 253, 253, 253, 254, 254, 254, 255, 255, 255]], self._bpl_mock.palettes)

        # Confirm output / BMA mappings
        # The tiles will be returned from the mock, so they won't match, they will be the unchanged
        # BPC tiles for this test! But that's ok. We confirmed the correct BPL and BPC changes above.
        self.assertImagesEqual(
            self._fix_path_expected("from_pil", "0.png"), self.two_layers.to_pil_single_layer(
                self._bpc_mock, self._bpl_mock.palettes, self._bpas, 0
            )
        )
        reloaded = self._save_and_reload_main_fixture(self.two_layers)
        self.assertEqual(self.two_layers.layer0, reloaded.layer0)
        self.assertEqual(self.two_layers.layer1, reloaded.layer1)

    def test_from_pil_hybrid_palettes(self) -> None:
        self._bpc_mock.mock__enable_writing()
        self._bpl_mock.mock__enable_writing()
        self.two_layers.from_pil(
            self._bpc_mock, self._bpl_mock,
            self._load_image(self._fix_path_layer_import_lower()),
            self._load_image(self._fix_path_layer_import_upper_extended_pal()),
            how_many_palettes_lower_layer=6
        )

        # Confirm BPL and BPC changes
        self.assertEqual(1, self._bpc_mock.tile_variant_1_written_to)
        self.assertEqual(0, self._bpc_mock.tile_variant_2_written_to)
        self.assertEqual(1, self._bpc_mock.tilemaps_variant_1_written_to)
        self.assertEqual(None, self._bpc_mock.tilemaps_variant_2_written_to)
        self.assertEqual(0, self._bpc_mock.tilemaps_variant_3_written_to)
        self.assertEqual([[44, 151, 205, 176, 222, 58, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 176, 255, 157, 255, 255, 255, 136, 136, 136, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 0, 255, 222, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 18, 171, 86, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [250, 255, 0, 0, 22, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 255, 255, 255, 136, 136, 136, 176, 255, 157, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 176, 222, 58, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 176, 255, 157, 255, 255, 255, 136, 136, 136, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 0, 255, 222, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 18, 171, 86, 255, 255, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [250, 255, 0, 0, 22, 255, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [44, 151, 205, 255, 255, 255, 136, 136, 136, 176, 255, 157, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [255, 0, 0, 255, 157, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], self._bpl_mock.palettes)

        reloaded = self._save_and_reload_main_fixture(self.two_layers)
        self.assertEqual(self.two_layers.layer0, reloaded.layer0)
        self.assertEqual(self.two_layers.layer1, reloaded.layer1)

    def test_from_pil_wrong_size(self) -> None:
        with self.assertRaises(ValueError):
            self.two_layers.from_pil(
                self._bpc_mock, self._bpl_mock, self._load_image(self._fix_path_layer_import_wrong_size()), None
            )

    def test_remove_upper_layer(self) -> None:
        self.assertIsNotNone(self.two_layers.layer1)
        self.assertEqual(2, self.two_layers.number_of_layers)
        self.two_layers.remove_upper_layer()
        self.assertIsNone(self.two_layers.layer1)
        self.assertEqual(1, self.two_layers.number_of_layers)
        saved = self._save_and_reload_main_fixture(self.two_layers)
        self.assertIsNone(saved.layer1)
        self.assertEqual(1, saved.number_of_layers)

        self.assertIsNone(self.single_layer.layer1)
        self.assertEqual(1, self.single_layer.number_of_layers)
        self.single_layer.remove_upper_layer()
        self.assertIsNone(self.single_layer.layer1)
        self.assertEqual(1, self.single_layer.number_of_layers)
        saved = self._save_and_reload_main_fixture(self.single_layer)
        self.assertIsNone(saved.layer1)
        self.assertEqual(1, saved.number_of_layers)

    def test_add_upper_layer(self) -> None:
        self.assertIsNotNone(self.two_layers.layer1)
        self.assertEqual(2, self.two_layers.number_of_layers)
        self.two_layers.add_upper_layer()
        self.assertIsNotNone(self.two_layers.layer1)
        self.assertEqual(2, self.two_layers.number_of_layers)
        saved = self._save_and_reload_main_fixture(self.two_layers)
        self.assertIsNotNone(saved.layer1)
        self.assertEqual(2, saved.number_of_layers)

        self.assertIsNone(self.single_layer.layer1)
        self.assertEqual(1, self.single_layer.number_of_layers)
        self.single_layer.add_upper_layer()
        self.assertIsNotNone(self.single_layer.layer1)
        self.assertEqual(2, self.single_layer.number_of_layers)
        saved = self._save_and_reload_main_fixture(self.single_layer)
        self.assertIsNotNone(saved.layer1)
        self.assertEqual(2, saved.number_of_layers)

    def test_resize(self) -> None:
        self.two_layers.resize(10, 11, 12, 13)
        self.assertEqual(10, self.two_layers.map_width_chunks)
        self.assertEqual(11, self.two_layers.map_height_chunks)
        self.assertEqual(12, self.two_layers.map_width_camera)
        self.assertEqual(13, self.two_layers.map_height_camera)

        self.assertImagesEqual(
            self._fix_path_expected("resize", "0.png"), self.two_layers.to_pil_single_layer(
                self._bpc_mock, self._bpl_mock.palettes, self._bpas, 0
            )
        )
        self.assertImagesEqual(
            self._fix_path_expected("resize", "1.png"), self.two_layers.to_pil_single_layer(
                self._bpc_mock, self._bpl_mock.palettes, self._bpas, 1
            )
        )
        reloaded = self._save_and_reload_main_fixture(self.two_layers)
        self.assertEqual(self.two_layers.layer0, reloaded.layer0)
        self.assertEqual(self.two_layers.layer1, reloaded.layer1)
        self.assertEqual(10, reloaded.map_width_chunks)
        self.assertEqual(11, reloaded.map_height_chunks)
        self.assertEqual(12, reloaded.map_width_camera)
        self.assertEqual(13, reloaded.map_height_camera)

    def test_place_chunk(self) -> None:
        x = 12
        y = 3
        index = y * 16 + x
        self.assertEqual(30, self.two_layers.layer0[index])
        assert self.two_layers.layer1 is not None
        self.assertEqual(9, self.two_layers.layer1[index])
        self.two_layers.place_chunk(0, x, y, 13)
        self.assertEqual(13, self.two_layers.layer0[index])
        self.two_layers.place_chunk(1, x, y, 15)
        self.assertEqual(15, self.two_layers.layer1[index])
        saved = self._save_and_reload_main_fixture(self.two_layers)
        self.assertEqual(13, saved.layer0[index])
        assert saved.layer1 is not None
        self.assertEqual(15, saved.layer1[index])
        img = self.two_layers.to_pil_single_layer(self._bpc_mock, self._bpl_mock.palettes, self._bpas, 0)
        self.assertImagesEqual(
            self._fix_path_expected("place_chunk", "0.png"), img
        )
        img = self.two_layers.to_pil_single_layer(self._bpc_mock, self._bpl_mock.palettes, self._bpas, 1)
        self.assertImagesEqual(
            self._fix_path_expected("place_chunk", "1.png"), img
        )

    def test_place_collision(self) -> None:
        x = 12
        y = 3
        index = y * 48 + x
        assert self.two_layers_two_col.collision is not None
        self.assertEqual(False, self.two_layers_two_col.collision[index])
        assert self.two_layers_two_col.collision2 is not None
        self.assertEqual(False, self.two_layers_two_col.collision2[index])
        self.two_layers_two_col.place_collision(0, x, y, True)
        self.assertEqual(True, self.two_layers_two_col.collision[index])
        self.two_layers_two_col.place_collision(1, x, y, True)
        self.assertEqual(True, self.two_layers_two_col.collision2[index])

    def tet_place_data(self) -> None:
        x = 12
        y = 3
        index = y * 48 + x
        assert self.two_layers_two_col_data.unknown_data_block is not None
        self.assertEqual(0, self.two_layers_two_col_data.unknown_data_block[index])
        self.two_layers_two_col_data.place_data(x, y, 123)
        self.assertEqual(123, self.two_layers_two_col_data.unknown_data_block[index])

    def test_metadata(self) -> None:
        layer0 = [1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 1, 1, 1, 1, 1, 1, 1, 10, 11, 12, 13, 14, 15, 16, 17, 1, 1, 1, 1, 1, 1, 1, 1, 18, 19, 20, 21, 22, 23, 24, 25, 1, 1, 1, 1, 1, 1, 1, 1, 26, 27, 28, 29, 30, 31, 32, 33, 1, 1, 1, 1, 1, 1, 1, 1, 34, 35, 36, 37, 38, 39, 40, 41, 1, 1, 1, 1, 1, 1, 1, 1, 42, 43, 44, 45, 46, 47, 48, 49, 1, 1, 1, 1, 1, 1, 1, 1, 50, 51, 52, 53, 54, 55, 56, 57, 1, 1, 1, 1, 1, 1, 1, 1, 58, 59, 60, 61, 62, 63, 64, 65, 1, 1, 1, 1, 1, 1, 1, 1, 66, 67, 68, 69, 70, 71, 72, 73, 1, 1, 1, 1, 1, 1, 1, 1, 74, 75, 76, 77, 78, 79, 80, 81, 1, 1, 1, 1, 1, 1, 1, 1, 82, 83, 84, 85, 86, 87, 88, 89]
        layer1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 9, 9, 9, 9, 9, 9, 9, 10, 11, 12, 13, 14, 15, 16, 17, 9, 9, 9, 9, 9, 9, 9, 9, 18, 19, 20, 21, 22, 23, 24, 25, 9, 9, 9, 9, 9, 9, 9, 9, 26, 27, 28, 29, 30, 31, 32, 33, 9, 9, 9, 9, 9, 9, 9, 9, 34, 35, 36, 37, 38, 39, 40, 41, 9, 9, 9, 9, 9, 9, 9, 9, 42, 43, 44, 45, 46, 47, 48, 49, 9, 9, 9, 9, 9, 9, 9, 9, 50, 51, 52, 53, 54, 55, 56, 57, 9, 9, 9, 9, 9, 9, 9, 9, 58, 59, 60, 61, 62, 63, 64, 65, 9, 9, 9, 9, 9, 9, 9, 9, 66, 67, 68, 69, 70, 71, 72, 73, 9, 9, 9, 9, 9, 9, 9, 9, 74, 75, 76, 77, 78, 79, 80, 81, 9, 9, 9, 9, 9, 9, 9, 9, 82, 83, 84, 85, 86, 87, 88, 89, 9, 9, 9, 9, 9, 9, 9, 9]
        data_block = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 25, 25, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 25, 25, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 25, 25, 25, 25, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 16, 0, 0, 0, 0, 0, 0, 0, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 16, 0, 0, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 116, 0, 0, 0, 0, 0, 0, 0, 0, 66, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 66, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 6, 6, 0, 0, 0, 2, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 6, 6, 6, 6, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 6, 0, 0, 6, 0, 0, 0, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 6, 6, 6, 0, 0, 0, 2, 2, 2, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        col1 = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
        col2 = [False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, False, False, True, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, True, True, True, False, False, False, False, False, False, False, False, True, True, False, True, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, True, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, False, True, True, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, True, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False]
        
        def two_layers(model: BmaProtocol):
            self.assertEqual(48, model.map_width_camera)
            self.assertEqual(33, model.map_height_camera)
            self.assertEqual(3, model.tiling_width)
            self.assertEqual(3, model.tiling_height)
            self.assertEqual(16, model.map_width_chunks)
            self.assertEqual(11, model.map_height_chunks)
            self.assertEqual(2, model.number_of_layers)
            self.assertEqual(0, model.unk6)
            self.assertEqual(0, model.number_of_collision_layers)
            self.assertEqual(layer0, model.layer0)
            self.assertEqual(layer1, model.layer1)
            self.assertEqual(None, model.unknown_data_block)
            self.assertEqual(None, model.collision)
            self.assertEqual(None, model.collision2)

        def two_layers_two_col_data(model: BmaProtocol):
            self.assertEqual(48, model.map_width_camera)
            self.assertEqual(33, model.map_height_camera)
            self.assertEqual(3, model.tiling_width)
            self.assertEqual(3, model.tiling_height)
            self.assertEqual(16, model.map_width_chunks)
            self.assertEqual(11, model.map_height_chunks)
            self.assertEqual(2, model.number_of_layers)
            self.assertEqual(1, model.unk6)
            self.assertEqual(2, model.number_of_collision_layers)
            self.assertEqual(layer0, model.layer0)
            self.assertEqual(layer1, model.layer1)
            self.assertEqual(data_block, model.unknown_data_block)
            self.assertEqual(col1, model.collision)
            self.assertEqual(col2, model.collision2)

        def single_layer(model: BmaProtocol):
            self.assertEqual(48, model.map_width_camera)
            self.assertEqual(33, model.map_height_camera)
            self.assertEqual(3, model.tiling_width)
            self.assertEqual(3, model.tiling_height)
            self.assertEqual(16, model.map_width_chunks)
            self.assertEqual(11, model.map_height_chunks)
            self.assertEqual(1, model.number_of_layers)
            self.assertEqual(0, model.unk6)
            self.assertEqual(0, model.number_of_collision_layers)
            self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 1, 1, 1, 1, 1, 1, 1, 10, 11, 12, 13, 14, 15, 16, 17, 1, 1, 1, 1, 1, 1, 1, 1, 18, 19, 20, 21, 22, 23, 24, 25, 1, 1, 1, 1, 1, 1, 1, 1, 26, 27, 28, 29, 30, 31, 32, 33, 1, 1, 1, 1, 1, 1, 1, 1, 34, 35, 36, 37, 38, 39, 40, 41, 1, 1, 1, 1, 1, 1, 1, 1, 42, 43, 44, 45, 46, 47, 48, 49, 1, 1, 1, 1, 1, 1, 1, 1, 50, 51, 52, 53, 54, 55, 56, 57, 1, 1, 1, 1, 1, 1, 1, 1, 58, 59, 60, 61, 62, 63, 64, 65, 1, 1, 1, 1, 1, 1, 1, 1, 66, 67, 68, 69, 70, 71, 72, 73, 1, 1, 1, 1, 1, 1, 1, 1, 74, 75, 76, 77, 78, 79, 80, 81, 1, 1, 1, 1, 1, 1, 1, 1, 82, 83, 84, 85, 86, 87, 88, 89], model.layer0)
            self.assertEqual(None, model.layer1)
            self.assertEqual(None, model.unknown_data_block)
            self.assertEqual(None, model.collision)
            self.assertEqual(None, model.collision2)

        def two_layers_one_col(model: BmaProtocol):
            self.assertEqual(48, model.map_width_camera)
            self.assertEqual(33, model.map_height_camera)
            self.assertEqual(3, model.tiling_width)
            self.assertEqual(3, model.tiling_height)
            self.assertEqual(16, model.map_width_chunks)
            self.assertEqual(11, model.map_height_chunks)
            self.assertEqual(2, model.number_of_layers)
            self.assertEqual(0, model.unk6)
            self.assertEqual(1, model.number_of_collision_layers)
            self.assertEqual(layer0, model.layer0)
            self.assertEqual(layer1, model.layer1)
            self.assertEqual(None, model.unknown_data_block)
            self.assertEqual(col1, model.collision)
            self.assertEqual(None, model.collision2)

        self._test_metadata_with_reload(self.two_layers, two_layers)
        self._test_metadata_with_reload(self.two_layers_two_col_data, two_layers_two_col_data)
        self._test_metadata_with_reload(self.single_layer, single_layer)
        self._test_metadata_with_reload(self.two_layers_one_col, two_layers_one_col)

    def _test_metadata_with_reload(self, model: BmaProtocol, cb: typing.Callable[[BmaProtocol], None]):
        cb(model)
        cb(self._save_and_reload_main_fixture(model))

    @romtest(file_ext='bma', path='MAP_BG/')
    def test_using_rom(self, _, file):
        bma_before = self.handler.deserialize(file)
        bma_after = self._save_and_reload_main_fixture(bma_before)

        self.assertEqual(bma_before.map_width_camera, bma_after.map_width_camera)
        self.assertEqual(bma_before.map_height_camera, bma_after.map_height_camera)
        self.assertEqual(bma_before.tiling_width, bma_after.tiling_width)
        self.assertEqual(bma_before.tiling_height, bma_after.tiling_height)
        self.assertEqual(bma_before.map_width_chunks, bma_after.map_width_chunks)
        self.assertEqual(bma_before.map_height_chunks, bma_after.map_height_chunks)
        self.assertEqual(bma_before.number_of_layers, bma_after.number_of_layers)
        self.assertEqual(bma_before.unk6, bma_after.unk6)
        self.assertEqual(bma_before.number_of_collision_layers, bma_after.number_of_collision_layers)
        self.assertEqual(bma_before.layer0, bma_after.layer0)
        self.assertEqual(bma_before.layer1, bma_after.layer1)
        self.assertEqual(bma_before.unknown_data_block, bma_after.unknown_data_block)
        self.assertEqual(bma_before.collision, bma_after.collision)
        self.assertEqual(bma_before.collision2, bma_after.collision2)

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_expected(cls, typ: str, file: str):
        return 'fixtures', 'expected', typ, file

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_single_layer(cls):
        return 'fixtures', 'single_layer.bma'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_two_layers(cls):
        return 'fixtures', 'two_layers.bma'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_single_layer_one_col(cls):
        return 'fixtures', 'single_layer_one_col.bma'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_two_layers_one_col(cls):
        return 'fixtures', 'two_layers_one_col.bma'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_two_layers_two_col(cls):
        return 'fixtures', 'two_layers_two_col.bma'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_two_layers_two_col_data(cls):
        return '..', '..', 'test', 'fixtures', 'MAP_BG', 'coco.bma'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_two_layers_data(cls):
        return 'fixtures', 'two_layers_data.bma'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_one_layer_two_col(cls):
        return 'fixtures', 'one_layer_two_col.bma'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_layer_import_lower(cls):
        return 'fixtures', 'layer_import_lower.png'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_layer_import_upper(cls):
        return 'fixtures', 'layer_import_upper.png'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_layer_import_upper_extended_pal(cls):
        return 'fixtures', 'layer_import_upper_extended_pal.png'

    @typing.no_type_check
    @classmethod
    @fixpath
    def _fix_path_layer_import_wrong_size(cls):
        return 'fixtures', 'layer_import_wrong_size.png'
