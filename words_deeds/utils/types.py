from dataclasses import dataclass, field


@dataclass
class Indicator:
    name: str
    more_dem: list[int] = field(default_factory=lambda: [])
    less_dem: list[int] = field(default_factory=lambda: [])


@dataclass
class DemocracyType:
    name: str
    vdem_index: str
    indicators: list[Indicator]
