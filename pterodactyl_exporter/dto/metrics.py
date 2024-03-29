from dataclasses import dataclass, field
from typing import List


@dataclass
class Metrics:
    name: List[str] = field(default_factory=list)
    id: List[str] = field(default_factory=list)
    memory: List[float] = field(default_factory=list)
    cpu: List[float] = field(default_factory=list)
    disk: List[float] = field(default_factory=list)
    rx: List[float] = field(default_factory=list)
    tx: List[float] = field(default_factory=list)
    uptime: List[float] = field(default_factory=list)
    max_memory: List[float] = field(default_factory=list)
    max_swap: List[float] = field(default_factory=list)
    max_disk: List[float] = field(default_factory=list)
    io: List[float] = field(default_factory=list)
    max_cpu: List[float] = field(default_factory=list)
    last_backup_time: List[float] = field(default_factory=list)

    def __iter__(self):
        fields = self.__dataclass_fields__.keys()
        for index in range(len(self.name)):
            item = {}
            for field_name in fields:
                item[field_name] = getattr(self, field_name)[index]
            yield item
