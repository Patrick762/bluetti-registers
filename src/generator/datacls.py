from dataclasses import dataclass

@dataclass
class DataField():
    name: str
    start: int
    datatype: str = "uint"
    lenght: int = 1
    scaling: float = 1

@dataclass
class DataProtocol():
    version: int
    comm_type: str
    fields: list[DataField]
