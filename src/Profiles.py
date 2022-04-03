from dataclasses import dataclass, field


@dataclass
class Vib:
    name: str
    version: str


Vibs = list[Vib]


@dataclass
class Profile:
    apply_date: str = ''
    operation: str = ''
    vibs: Vibs = field(default_factory=list)


@dataclass
class Profiles:
    profiles: dict[str, list[Profile]] = field(default_factory=dict)
