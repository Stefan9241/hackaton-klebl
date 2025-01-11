from dataclasses import dataclass


@dataclass
class Dimensions:
    length: str
    width: str
    height: str


@dataclass
class DrawingMetadata:
    plan_key: str
    stat_pos: str
    auftr_number: str
    index: str
    prefabbed_position: str
    amount: int
    dimensions: Dimensions
    volume: float
    weight: float


@dataclass
class Part:
    position: str
    amount: int
    designation: str


@dataclass
class SteelPosition:
    position: int
    anz: int
    length: float
    bem: str


@dataclass
class SteelDescription:
    steel_type: str
    total_weight: float
    positions_list: list[SteelPosition]


@dataclass
class ParsedDrawing:
    metadata: DrawingMetadata
    parts: list[Part]
    steel_list: list[SteelDescription]
