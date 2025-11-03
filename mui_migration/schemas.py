from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class MUIProp:
    name: str
    type: Optional[str] = None
    default: Optional[str] = None
    required: bool = False
    description: Optional[str] = None
    values: Optional[List[str]] = None


@dataclass
class MUIEvent:
    name: str
    description: Optional[str] = None


@dataclass
class MUIComponent:
    name: str
    import_path: str
    description: Optional[str] = None
    props: List[MUIProp] = field(default_factory=list)
    events: List[MUIEvent] = field(default_factory=list)
    slots: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PropMapping:
    from_prop: str
    to_attribute: Optional[str] = None
    value_map: Optional[Dict[str, Any]] = None
    default: Optional[Any] = None
    notes: Optional[str] = None


@dataclass
class EventMapping:
    from_event: str
    to_event: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class MappingCoverage:
    mapped_props: List[str] = field(default_factory=list)
    unmapped_props: List[str] = field(default_factory=list)
    mapped_events: List[str] = field(default_factory=list)
    unmapped_events: List[str] = field(default_factory=list)


@dataclass
class ComponentMapping:
    mui_component: str
    modus_tag: Optional[str]
    prop_mappings: List[PropMapping] = field(default_factory=list)
    event_mappings: List[EventMapping] = field(default_factory=list)
    structure: Optional[str] = None
    coverage: MappingCoverage = field(default_factory=MappingCoverage)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "muiComponent": self.mui_component,
            "modusTag": self.modus_tag,
            "propMappings": [asdict(p) for p in self.prop_mappings],
            "eventMappings": [asdict(e) for e in self.event_mappings],
            "structure": self.structure,
            "coverage": asdict(self.coverage),
        }


def camel_to_kebab(value: str) -> str:
    result_chars: List[str] = []
    for char in value:
        if char.isupper():
            result_chars.append("-")
            result_chars.append(char.lower())
        else:
            result_chars.append(char)
    result = "".join(result_chars)
    return result.lstrip("-")


def normalize_prop_name(value: str) -> str:
    return camel_to_kebab(value).replace("_", "-").lower()


