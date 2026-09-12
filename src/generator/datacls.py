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

    def to_dict(self):
        return {
            "name": self.name,
            "start": self.start,
            "datatype": self.datatype,
            "length": self.length,
            "scaling": self.scaling,
            "writeable": self.writeable,
        }


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
