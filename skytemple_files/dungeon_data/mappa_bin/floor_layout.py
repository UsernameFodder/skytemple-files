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
from xml.etree.ElementTree import Element

import typing

from range_typed_integers import i8_checked, u8_checked, u16_checked, i16_checked

from skytemple_files.common.util import *
from skytemple_files.common.xml_util import XmlSerializable, validate_xml_tag, XmlValidateError, validate_xml_attribs
from skytemple_files.dungeon_data.mappa_bin import *
from skytemple_files.common.i18n_util import f, _

if TYPE_CHECKING:
    from skytemple_files.dungeon_data.mappa_bin.model import MappaBinReadContainer


class MappaFloorStructureType(Enum):
    MEDIUM_LARGE = 0, _("Medium Large")  # Max 6x4
    SMALL = 1, _("Small")  # Max 2x3
    SINGLE_MONSTER_HOUSE = 2, _("Single Monster House")
    RING = 3, _("Ring")  # Outer ring with 8 rooms inside in a 4 x 2 shape
    CROSSROADS = 4, _("Crossroads")  # Crossroads (3 rooms at the top, 3 at the bottom, 2 on each side)
    TWO_ROOMS_ONE_MH = 5, _("Two Rooms, One Monster House")  # Two rooms, one is a monster house
    LINE = 6, _("Line")  # 1 horizontal line with 5 rooms in a row
    CROSS = 7, _("Cross")  # 5 rooms: up, down, left, right, center
    SMALL_MEDIUM = 8, _("Small Medium")  # Max. 4x2
    BETTLE = 9, _("Beetle")  # 1 big room in the center with 3 a on each side
    OUTER_ROOMS = 10, _("Outer Rooms")  # All the rooms are in the map borders, none in the center (Max 6x4)
    MEDIUM = 11, _("Medium")  # Max 3x3
    MEDIUM_LARGE_12 = 12, _("Medium Large (12)")  # Max 6x4
    MEDIUM_LARGE_13 = 13, _("Medium Large (13)")  # Max 6x4
    MEDIUM_LARGE_14 = 14, _("Medium Large (14)")  # Max 6x4
    MEDIUM_LARGE_15 = 15, _("Medium Large (15)")  # Max 6x4

    @property
    def print_name(self):
        return self._print_name_

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, print_name: typing.Optional[str] = None):
        self._print_name_: str = print_name  # type: ignore

    def __str__(self):
        return self._print_name_

    def __repr__(self):
        return f'MappaFloorStructureType.{self.name}'


class MappaFloorWeather(Enum):
    CLEAR = 0, _("Clear")
    SUNNY = 1, _("Sunny")
    SANDSTORM = 2, _("Sandstorm")
    CLOUDY = 3, _("Cloudy")
    RAINY = 4, _("Rainy")
    HAIL = 5, _("Hail")
    FOG = 6, _("Fog")
    SNOW = 7, _("Snow")
    RANDOM = 8, _("Random")

    @property
    def print_name(self):
        return self._print_name_

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, print_name: str = None):
        self._print_name_ = print_name

    def __str__(self):
        return self._print_name_

    def __repr__(self):
        return f'MappaFloorWeather.{self.name}'


class MappaFloorTerrainSettings:
    def __init__(
            self, has_secondary_terrain: bool, unk1: bool, generate_imperfect_rooms: bool,
            unk3: bool, unk4: bool, unk5: bool, unk6: bool, unk7: bool
    ):
        self.has_secondary_terrain = has_secondary_terrain
        # Seems unused.
        self.unk1 = unk1
        self.generate_imperfect_rooms = generate_imperfect_rooms
        # These bits might just be fully unused.
        self.unk3 = unk3
        self.unk4 = unk4
        self.unk5 = unk5
        self.unk6 = unk6
        self.unk7 = unk7

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MappaFloorTerrainSettings):
            return False
        return self.has_secondary_terrain == other.has_secondary_terrain \
            and self.unk1 == other.unk1 \
            and self.generate_imperfect_rooms == other.generate_imperfect_rooms \
            and self.unk3 == other.unk3 \
            and self.unk4 == other.unk4 \
            and self.unk5 == other.unk5 \
            and self.unk6 == other.unk6 \
            and self.unk7 == other.unk7

    def to_mappa(self):
        return u8(generate_bitfield((self.unk7, self.unk6, self.unk5, self.unk4, self.unk3, self.generate_imperfect_rooms,
                                     self.unk1, self.has_secondary_terrain)))


class MappaFloorDarknessLevel(Enum):
    NO_DARKNESS = 0, _("No darkness")
    HEAVY_DARKNESS = 1, _("1-tile vision (Heavy darkness)")
    LIGHT_DARKNESS = 2, _("2-tile vision (Light darkness)")
    THREE_TILE = 3, _("3-tile vision")
    FOUR_TILE = 4, _("4-tile vision")

    def __new__(cls, *args, **kwargs):  # type: ignore
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    # ignore the first param since it's already set by __new__
    def __init__(self, _: int, print_name: str = None):
        self._print_name_ = print_name

    def __str__(self):
        return self._print_name_

    def __repr__(self):
        return f'MappaFloorDarknessLevel.{self.name}'

    @property
    def print_name(self):
        return self._print_name_


class MappaFloorLayout(AutoString, XmlSerializable, CheckedIntWrites):
    structure: MappaFloorStructureType
    room_density: i8
    tileset_id: u8
    music_id: u8
    weather: MappaFloorWeather
    floor_connectivity: u8
    initial_enemy_density: i8
    kecleon_shop_chance: u8
    monster_house_chance: u8
    unusued_chance: u8
    sticky_item_chance: u8
    dead_ends: bool
    secondary_terrain: u8
    terrain_settings: MappaFloorTerrainSettings
    unk_e: bool
    item_density: u8
    trap_density: u8
    floor_number: u8
    fixed_floor_id: u8
    extra_hallway_density: u8
    buried_item_density: u8
    water_density: u8
    darkness_level: MappaFloorDarknessLevel
    max_coin_amount: int
    kecleon_shop_item_positions: u8
    empty_monster_house_chance: u8
    unk_hidden_stairs: u8
    hidden_stairs_spawn_chance: u8
    enemy_iq: u16
    iq_booster_boost: i16

    def __init__(
            self, *, structure: MappaFloorStructureType, room_density: i8, tileset_id: u8, music_id: u8,
            weather: MappaFloorWeather, floor_connectivity: u8, initial_enemy_density: i8, kecleon_shop_chance: u8,
            monster_house_chance: u8, unusued_chance: u8, sticky_item_chance: u8, dead_ends: bool,
            secondary_terrain: u8, terrain_settings: MappaFloorTerrainSettings,
            unk_e: bool, item_density: u8, trap_density: u8, floor_number: u8, fixed_floor_id: u8,
            extra_hallway_density: u8, buried_item_density: u8, water_density: u8,
            darkness_level: MappaFloorDarknessLevel, max_coin_amount: int, kecleon_shop_item_positions: u8,
            empty_monster_house_chance: u8, unk_hidden_stairs: u8, hidden_stairs_spawn_chance: u8, enemy_iq: u16,
            iq_booster_boost: i16
    ):
        self.structure = structure
        self.room_density = room_density
        self.tileset_id = tileset_id
        self.music_id = music_id
        self.weather = weather
        self.floor_connectivity = floor_connectivity
        self.initial_enemy_density = initial_enemy_density
        self.kecleon_shop_chance = kecleon_shop_chance
        self.monster_house_chance = monster_house_chance
        self.unusued_chance = unusued_chance
        self.sticky_item_chance = sticky_item_chance
        self.dead_ends = dead_ends
        self.secondary_terrain = secondary_terrain
        self.terrain_settings = terrain_settings
        self.unk_e = unk_e
        self.item_density = item_density
        self.trap_density = trap_density
        self.floor_number = floor_number
        self.fixed_floor_id = fixed_floor_id
        self.extra_hallway_density = extra_hallway_density
        self.buried_item_density = buried_item_density
        self.water_density = water_density
        self.darkness_level = darkness_level
        self.max_coin_amount = max_coin_amount
        self.kecleon_shop_item_positions = kecleon_shop_item_positions
        self.empty_monster_house_chance = empty_monster_house_chance
        self.unk_hidden_stairs = unk_hidden_stairs
        self.hidden_stairs_spawn_chance = hidden_stairs_spawn_chance
        self.enemy_iq = enemy_iq
        # If <=0: Disabled
        self.iq_booster_boost = iq_booster_boost

    @classmethod
    def from_mappa(cls, read: 'MappaBinReadContainer', pointer: int):
        terrain_settings_bitflag = read_u8(read.data, pointer + 0x0D)
        terrain_settings = MappaFloorTerrainSettings(
            *(bool(terrain_settings_bitflag >> i & 1) for i in range(8))
        )
        return cls(
            structure=MappaFloorStructureType(read_u8(read.data, pointer + 0x00)),
            room_density=read_i8(read.data, pointer + 0x01),
            tileset_id=read_u8(read.data, pointer + 0x02),
            music_id=read_u8(read.data, pointer + 0x03),
            weather=MappaFloorWeather(read_u8(read.data, pointer + 0x04)),
            floor_connectivity=read_u8(read.data, pointer + 0x05),
            initial_enemy_density=read_i8(read.data, pointer + 0x06),
            kecleon_shop_chance=read_u8(read.data, pointer + 0x07),
            monster_house_chance=read_u8(read.data, pointer + 0x08),
            unusued_chance=read_u8(read.data, pointer + 0x09),
            sticky_item_chance=read_u8(read.data, pointer + 0x0A),
            dead_ends=bool(read_u8(read.data, pointer + 0x0B)),
            secondary_terrain=read_u8(read.data, pointer + 0x0C),
            terrain_settings=terrain_settings,
            unk_e=bool(read_u8(read.data, pointer + 0x0E)),
            item_density=read_u8(read.data, pointer + 0x0F),
            trap_density=read_u8(read.data, pointer + 0x10),
            floor_number=read_u8(read.data, pointer + 0x11),
            fixed_floor_id=read_u8(read.data, pointer + 0x12),
            extra_hallway_density=read_u8(read.data, pointer + 0x13),
            buried_item_density=read_u8(read.data, pointer + 0x14),
            water_density=read_u8(read.data, pointer + 0x15),
            darkness_level=MappaFloorDarknessLevel(read_u8(read.data, pointer + 0x16)),
            max_coin_amount=read_u8(read.data, pointer + 0x17) * 5,
            kecleon_shop_item_positions=read_u8(read.data, pointer + 0x18),
            empty_monster_house_chance=read_u8(read.data, pointer + 0x19),
            unk_hidden_stairs=read_u8(read.data, pointer + 0x1A),
            hidden_stairs_spawn_chance=read_u8(read.data, pointer + 0x1B),
            enemy_iq=read_u16(read.data, pointer + 0x1C),
            iq_booster_boost=read_i16(read.data, pointer + 0x1E)
        )

    def to_mappa(self) -> bytes:
        data = bytearray(32)
        write_u8(data, self.structure.value, 0x00)
        write_i8(data, self.room_density, 0x01)
        write_u8(data, self.tileset_id, 0x02)
        write_u8(data, self.music_id, 0x03)
        write_u8(data, self.weather.value, 0x04)
        write_u8(data, self.floor_connectivity, 0x05)
        write_i8(data, self.initial_enemy_density, 0x06)
        write_u8(data, self.kecleon_shop_chance, 0x07)
        write_u8(data, self.monster_house_chance, 0x08)
        write_u8(data, self.unusued_chance, 0x09)
        write_u8(data, self.sticky_item_chance, 0x0A)
        write_u8(data, u8(int(self.dead_ends)), 0x0B)
        write_u8(data, self.secondary_terrain, 0x0C)
        write_u8(data, self.terrain_settings.to_mappa(), 0x0D)
        write_u8(data, u8(int(self.unk_e)), 0x0E)
        write_u8(data, self.item_density, 0x0F)
        write_u8(data, self.trap_density, 0x10)
        write_u8(data, self.floor_number, 0x11)
        write_u8(data, self.fixed_floor_id, 0x12)
        write_u8(data, self.extra_hallway_density, 0x13)
        write_u8(data, self.buried_item_density, 0x14)
        write_u8(data, self.water_density, 0x15)
        write_u8(data, self.darkness_level.value, 0x16)
        write_u8(data, u8(self.max_coin_amount // 5), 0x17)
        write_u8(data, self.kecleon_shop_item_positions, 0x18)
        write_u8(data, self.empty_monster_house_chance, 0x19)
        write_u8(data, self.unk_hidden_stairs, 0x1A)
        write_u8(data, self.hidden_stairs_spawn_chance, 0x1B)
        write_u16(data, self.enemy_iq, 0x1C)
        write_i16(data, self.iq_booster_boost, 0x1E)

        return data

    def to_xml(self) -> Element:
        xml_layout = Element(XML_FLOOR_LAYOUT, {
            XML_FLOOR_LAYOUT__STRUCTURE: self.structure.name,
            XML_FLOOR_LAYOUT__TILESET: str(self.tileset_id),
            XML_FLOOR_LAYOUT__BGM: str(self.music_id),
            XML_FLOOR_LAYOUT__WEATHER: self.weather.name,
            XML_FLOOR_LAYOUT__NUMBER: str(self.floor_number),
            XML_FLOOR_LAYOUT__FIXED_FLOOR_ID: str(self.fixed_floor_id),
            XML_FLOOR_LAYOUT__DARKNESS_LEVEL: self.darkness_level.name
        })
        xml_generator_settings = Element(XML_FLOOR_LAYOUT__GENSET, {
            XML_FLOOR_LAYOUT__GENSET__ROOM_DENSITY: str(self.room_density),
            XML_FLOOR_LAYOUT__GENSET__FLOOR_CONNECTIVITY: str(self.floor_connectivity),
            XML_FLOOR_LAYOUT__GENSET__INITIAL_ENEMY_DENSITY: str(self.initial_enemy_density),
            XML_FLOOR_LAYOUT__GENSET__DEAD_ENDS: str(int(self.dead_ends)),
            XML_FLOOR_LAYOUT__GENSET__ITEM_DENSITY: str(self.item_density),
            XML_FLOOR_LAYOUT__GENSET__TRAP_DENSITY: str(self.trap_density),
            XML_FLOOR_LAYOUT__GENSET__EXTRA_HALLWAY_DENSITY: str(self.extra_hallway_density),
            XML_FLOOR_LAYOUT__GENSET__BURIED_ITEM_DENSITY: str(self.buried_item_density),
            XML_FLOOR_LAYOUT__GENSET__WATER_DENSITY: str(self.water_density),
            XML_FLOOR_LAYOUT__GENSET__MAX_COIN_AMOUNT: str(self.max_coin_amount)
        })
        xml_chances = Element(XML_FLOOR_LAYOUT__CHANCES, {
            XML_FLOOR_LAYOUT__CHANCES__SHOP: str(self.kecleon_shop_chance),
            XML_FLOOR_LAYOUT__CHANCES__MONSTER_HOUSE: str(self.monster_house_chance),
            XML_FLOOR_LAYOUT__CHANCES__UNUSED: str(self.unusued_chance),
            XML_FLOOR_LAYOUT__CHANCES__STICKY_ITEM: str(self.sticky_item_chance),
            XML_FLOOR_LAYOUT__CHANCES__EMPTY_MONSTER_HOUSE: str(self.empty_monster_house_chance),
            XML_FLOOR_LAYOUT__CHANCES__HIDDEN_STAIRS: str(self.hidden_stairs_spawn_chance)
        })
        xml_terrain_settings = Element(XML_FLOOR_LAYOUT__TERRAINSET, {
            XML_FLOOR_LAYOUT__TERRAINSET__SECONDARY_USED: str(int(self.terrain_settings.has_secondary_terrain)),
            XML_FLOOR_LAYOUT__TERRAINSET__SECONDARY_TYPE: str(self.secondary_terrain),
            XML_FLOOR_LAYOUT__TERRAINSET__IMPERFECT_ROOMS: str(int(self.terrain_settings.generate_imperfect_rooms)),
            XML_FLOOR_LAYOUT__TERRAINSET__UNK1: str(int(self.terrain_settings.unk1)),
            XML_FLOOR_LAYOUT__TERRAINSET__UNK3: str(int(self.terrain_settings.unk3)),
            XML_FLOOR_LAYOUT__TERRAINSET__UNK4: str(int(self.terrain_settings.unk4)),
            XML_FLOOR_LAYOUT__TERRAINSET__UNK5: str(int(self.terrain_settings.unk5)),
            XML_FLOOR_LAYOUT__TERRAINSET__UNK6: str(int(self.terrain_settings.unk6)),
            XML_FLOOR_LAYOUT__TERRAINSET__UNK7: str(int(self.terrain_settings.unk7))
        })
        xml_misc = Element(XML_FLOOR_LAYOUT__MISCSET, {
            XML_FLOOR_LAYOUT__MISCSET__UNKE: str(int(self.unk_e)),
            XML_FLOOR_LAYOUT__MISCSET__KECLEON_SHOP_ITEM_POSITIONS: str(self.kecleon_shop_item_positions),
            XML_FLOOR_LAYOUT__MISCSET__UNK_HIDDEN_STAIRS: str(self.unk_hidden_stairs),
            XML_FLOOR_LAYOUT__MISCSET__ENEMY_IQ: str(self.enemy_iq),
            XML_FLOOR_LAYOUT__MISCSET__IQ_BOOSTER_BOOST: str(self.iq_booster_boost)
        })

        xml_layout.append(xml_generator_settings)
        xml_layout.append(xml_chances)
        xml_layout.append(xml_terrain_settings)
        xml_layout.append(xml_misc)

        return xml_layout

    @classmethod
    @typing.no_type_check
    def from_xml(cls, ele: Element) -> 'MappaFloorLayout':
        validate_xml_tag(ele, XML_FLOOR_LAYOUT)
        generator_settings = None
        chances = None
        terrain_settings = None
        misc = None
        for child in ele:
            if child.tag == XML_FLOOR_LAYOUT__GENSET:
                generator_settings = child
            elif child.tag == XML_FLOOR_LAYOUT__CHANCES:
                chances = child
            elif child.tag == XML_FLOOR_LAYOUT__TERRAINSET:
                terrain_settings = child
            elif child.tag == XML_FLOOR_LAYOUT__MISCSET:
                misc = child
            else:
                raise XmlValidateError(f(_("Unexpected sub-node for {XML_FLOOR_LAYOUT}: {child.tag}")))

        if generator_settings is None:
            raise XmlValidateError(f(_("{XML_FLOOR_LAYOUT__GENSET} missing for {XML_FLOOR_LAYOUT}.")))

        if chances is None:
            raise XmlValidateError(f(_("{XML_FLOOR_LAYOUT__CHANCES} missing for {XML_FLOOR_LAYOUT}.")))

        if terrain_settings is None:
            raise XmlValidateError(f(_("{XML_FLOOR_LAYOUT__TERRAINSET} missing for {XML_FLOOR_LAYOUT}.")))

        if misc is None:
            raise XmlValidateError(f(_("{XML_FLOOR_LAYOUT__MISCSET} missing for {XML_FLOOR_LAYOUT}.")))

        validate_xml_attribs(ele, [
            XML_FLOOR_LAYOUT__STRUCTURE,
            XML_FLOOR_LAYOUT__TILESET,
            XML_FLOOR_LAYOUT__BGM,
            XML_FLOOR_LAYOUT__WEATHER,
            XML_FLOOR_LAYOUT__NUMBER,
            XML_FLOOR_LAYOUT__FIXED_FLOOR_ID,
            XML_FLOOR_LAYOUT__DARKNESS_LEVEL
        ])

        validate_xml_attribs(generator_settings, [
            XML_FLOOR_LAYOUT__GENSET__ROOM_DENSITY,
            XML_FLOOR_LAYOUT__GENSET__FLOOR_CONNECTIVITY,
            XML_FLOOR_LAYOUT__GENSET__INITIAL_ENEMY_DENSITY,
            XML_FLOOR_LAYOUT__GENSET__DEAD_ENDS,
            XML_FLOOR_LAYOUT__GENSET__ITEM_DENSITY,
            XML_FLOOR_LAYOUT__GENSET__TRAP_DENSITY,
            XML_FLOOR_LAYOUT__GENSET__EXTRA_HALLWAY_DENSITY,
            XML_FLOOR_LAYOUT__GENSET__BURIED_ITEM_DENSITY,
            XML_FLOOR_LAYOUT__GENSET__WATER_DENSITY,
            XML_FLOOR_LAYOUT__GENSET__MAX_COIN_AMOUNT
        ])

        validate_xml_attribs(chances, [
            XML_FLOOR_LAYOUT__CHANCES__SHOP,
            XML_FLOOR_LAYOUT__CHANCES__MONSTER_HOUSE,
            XML_FLOOR_LAYOUT__CHANCES__UNUSED,
            XML_FLOOR_LAYOUT__CHANCES__STICKY_ITEM,
            XML_FLOOR_LAYOUT__CHANCES__EMPTY_MONSTER_HOUSE,
            XML_FLOOR_LAYOUT__CHANCES__HIDDEN_STAIRS
        ])

        validate_xml_attribs(terrain_settings, [
            XML_FLOOR_LAYOUT__TERRAINSET__SECONDARY_USED,
            XML_FLOOR_LAYOUT__TERRAINSET__SECONDARY_TYPE,
            XML_FLOOR_LAYOUT__TERRAINSET__IMPERFECT_ROOMS,
            XML_FLOOR_LAYOUT__TERRAINSET__UNK1,
            XML_FLOOR_LAYOUT__TERRAINSET__UNK3,
            XML_FLOOR_LAYOUT__TERRAINSET__UNK4,
            XML_FLOOR_LAYOUT__TERRAINSET__UNK5,
            XML_FLOOR_LAYOUT__TERRAINSET__UNK6,
            XML_FLOOR_LAYOUT__TERRAINSET__UNK7
        ])

        validate_xml_attribs(misc, [
            XML_FLOOR_LAYOUT__MISCSET__UNKE,
            XML_FLOOR_LAYOUT__MISCSET__KECLEON_SHOP_ITEM_POSITIONS,
            XML_FLOOR_LAYOUT__MISCSET__UNK_HIDDEN_STAIRS,
            XML_FLOOR_LAYOUT__MISCSET__ENEMY_IQ,
            XML_FLOOR_LAYOUT__MISCSET__IQ_BOOSTER_BOOST
        ])

        if not hasattr(MappaFloorStructureType, ele.get(XML_FLOOR_LAYOUT__STRUCTURE)):
            raise XmlValidateError(f(_("Invalid structure type {ele.get(XML_FLOOR_LAYOUT__STRUCTURE)}")))
        structure = getattr(MappaFloorStructureType, ele.get(XML_FLOOR_LAYOUT__STRUCTURE))

        if not hasattr(MappaFloorWeather, ele.get(XML_FLOOR_LAYOUT__WEATHER)):
            raise XmlValidateError(f(_("Invalid weather type {ele.get(XML_FLOOR_LAYOUT__WEATHER)}")))
        weather = getattr(MappaFloorWeather, ele.get(XML_FLOOR_LAYOUT__WEATHER))

        if not hasattr(MappaFloorDarknessLevel, ele.get(XML_FLOOR_LAYOUT__DARKNESS_LEVEL)):
            raise XmlValidateError(f(_("Invalid darkness level type {ele.get(XML_FLOOR_LAYOUT__DARKNESS_LEVEL)}")))
        darkness_level = getattr(MappaFloorDarknessLevel, ele.get(XML_FLOOR_LAYOUT__DARKNESS_LEVEL))

        return cls(
            structure=structure,
            room_density=i8_checked(int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__ROOM_DENSITY))),
            tileset_id=u8_checked(int(ele.get(XML_FLOOR_LAYOUT__TILESET))),
            music_id=u8_checked(int(ele.get(XML_FLOOR_LAYOUT__BGM))),
            weather=weather,
            floor_connectivity=u8_checked(int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__FLOOR_CONNECTIVITY))),
            initial_enemy_density=i8_checked(int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__INITIAL_ENEMY_DENSITY))),
            kecleon_shop_chance=u8_checked(int(chances.get(XML_FLOOR_LAYOUT__CHANCES__SHOP))),
            monster_house_chance=u8_checked(int(chances.get(XML_FLOOR_LAYOUT__CHANCES__MONSTER_HOUSE))),
            unusued_chance=u8_checked(int(chances.get(XML_FLOOR_LAYOUT__CHANCES__UNUSED))),
            sticky_item_chance=u8_checked(int(chances.get(XML_FLOOR_LAYOUT__CHANCES__STICKY_ITEM))),
            dead_ends=bool(int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__DEAD_ENDS))),
            secondary_terrain=u8_checked(int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__SECONDARY_TYPE))),
            terrain_settings=MappaFloorTerrainSettings(
                has_secondary_terrain=bool(int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__SECONDARY_USED))),
                unk1=bool(int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__UNK1))),
                generate_imperfect_rooms=bool(int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__IMPERFECT_ROOMS))),
                unk3=bool(int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__UNK3))),
                unk4=bool(int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__UNK4))),
                unk5=bool(int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__UNK5))),
                unk6=bool(int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__UNK6))),
                unk7=bool(int(terrain_settings.get(XML_FLOOR_LAYOUT__TERRAINSET__UNK7))),
            ),
            unk_e=bool(int(misc.get(XML_FLOOR_LAYOUT__MISCSET__UNKE))),
            item_density=u8_checked(int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__ITEM_DENSITY))),
            trap_density=u8_checked(int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__TRAP_DENSITY))),
            floor_number=u8_checked(int(ele.get(XML_FLOOR_LAYOUT__NUMBER))),
            fixed_floor_id=u8_checked(int(ele.get(XML_FLOOR_LAYOUT__FIXED_FLOOR_ID))),
            extra_hallway_density=u8_checked(int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__EXTRA_HALLWAY_DENSITY))),
            buried_item_density=u8_checked(int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__BURIED_ITEM_DENSITY))),
            water_density=u8_checked(int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__WATER_DENSITY))),
            darkness_level=darkness_level,
            max_coin_amount=int(generator_settings.get(XML_FLOOR_LAYOUT__GENSET__MAX_COIN_AMOUNT)),
            kecleon_shop_item_positions=u8_checked(int(misc.get(XML_FLOOR_LAYOUT__MISCSET__KECLEON_SHOP_ITEM_POSITIONS))),
            empty_monster_house_chance=u8_checked(int(chances.get(XML_FLOOR_LAYOUT__CHANCES__EMPTY_MONSTER_HOUSE))),
            unk_hidden_stairs=u8_checked(int(misc.get(XML_FLOOR_LAYOUT__MISCSET__UNK_HIDDEN_STAIRS))),
            hidden_stairs_spawn_chance=u8_checked(int(chances.get(XML_FLOOR_LAYOUT__CHANCES__HIDDEN_STAIRS))),
            enemy_iq=u16_checked(int(misc.get(XML_FLOOR_LAYOUT__MISCSET__ENEMY_IQ))),
            iq_booster_boost=i16_checked(int(misc.get(XML_FLOOR_LAYOUT__MISCSET__IQ_BOOSTER_BOOST))),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MappaFloorLayout):
            return False
        return self.structure == other.structure \
               and self.room_density == other.room_density \
               and self.tileset_id == other.tileset_id \
               and self.music_id == other.music_id \
               and self.weather == other.weather \
               and self.floor_connectivity == other.floor_connectivity \
               and self.initial_enemy_density == other.initial_enemy_density \
               and self.kecleon_shop_chance == other.kecleon_shop_chance \
               and self.monster_house_chance == other.monster_house_chance \
               and self.unusued_chance == other.unusued_chance \
               and self.sticky_item_chance == other.sticky_item_chance \
               and self.dead_ends == other.dead_ends \
               and self.secondary_terrain == other.secondary_terrain \
               and self.terrain_settings == other.terrain_settings \
               and self.unk_e == other.unk_e \
               and self.item_density == other.item_density \
               and self.trap_density == other.trap_density \
               and self.floor_number == other.floor_number \
               and self.fixed_floor_id == other.fixed_floor_id \
               and self.extra_hallway_density == other.extra_hallway_density \
               and self.buried_item_density == other.buried_item_density \
               and self.water_density == other.water_density \
               and self.darkness_level == other.darkness_level \
               and self.max_coin_amount == other.max_coin_amount \
               and self.kecleon_shop_item_positions == other.kecleon_shop_item_positions \
               and self.empty_monster_house_chance == other.empty_monster_house_chance \
               and self.unk_hidden_stairs == other.unk_hidden_stairs \
               and self.hidden_stairs_spawn_chance == other.hidden_stairs_spawn_chance \
               and self.enemy_iq == other.enemy_iq \
               and self.iq_booster_boost == other.iq_booster_boost
