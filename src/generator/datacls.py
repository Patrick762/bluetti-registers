from dataclasses import dataclass
from typing import Any


@dataclass
class DataField:
    name: str
    start: int
    datatype: str = "uint"
    length: int = 1
    scaling: float = 1
    writeable: bool = False
    unit: str | None = None
    category: str | None = None
    """Category (config / diagnostic)"""
    sensor: str | None = None
    """Sensor type (power, voltage, ...)"""
    state_type: str | None = None
    """State type (measurement / increasing)"""

    def to_dict(self):
        d = {
            "name": self.name,
            "start": self.start,
            "datatype": self.datatype,
            "length": self.length,
            "scaling": self.scaling,
            "writeable": self.writeable,
        }

        if self.unit is not None:
            d["unit"] = self.unit

        if self.category is not None:
            d["category"] = self.category

        if self.sensor is not None:
            d["sensor"] = self.sensor

        if self.state_type is not None:
            d["state_type"] = self.state_type

        return d


@dataclass
class DataProtocol:
    version: int
    comm_type: str
    fields: list[DataField]

    def to_dict(self):
        return {
            "version": self.version,
            "comm_type": self.comm_type,
            "fields": [f.to_dict() for f in self.fields],
        }


@dataclass
class BluettiDevice:
    name: str
    proto_version: int
    comm_type: str
    fields: list[DataField]
    contributors: list[str]
    specififations: dict[str, Any]

    def to_dict(self):
        return {
            "name": self.name,
            "proto_version": self.proto_version,
            "comm_type": self.comm_type,
            "contributors": self.contributors,
            "specififations": self.specififations,
            "fields": [f.to_dict() for f in self.fields],
        }
