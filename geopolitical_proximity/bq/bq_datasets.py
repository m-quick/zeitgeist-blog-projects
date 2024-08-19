from dataclasses import dataclass


@dataclass
class Dataset:
    name: str


geopolitical_proximity = Dataset(name="geopolitical_proximity")
