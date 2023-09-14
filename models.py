from typing import List
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Token:
    id: str
    begin: int
    end: int
    text: str

@dataclass(frozen=True)
class LinkedEntity:
    id: str
    text: str

@dataclass(frozen=True)
class Entity(Token):
    semantic: str
    codemaps: dict
    section: str
    assertion: str
    linked_entities: List[LinkedEntity]

@dataclass(frozen=True)
class Relation(Token):
    semantic: str
    from_ent: str
    from_ent_text: str
    to_ent: str
    to_ent_text: str

@dataclass(frozen=True)
class NLPResult:
    filename: str = ""
    content: str = ""
    tokens: List[Token] = field(default_factory=list)
    sentences: List[Token] = field(default_factory=list)
    entities: List[Entity] = field(default_factory=list)
    relations: List[Relation] = field(default_factory=list)
    text_id: str = ""
    pipeline: dict = field(default_factory=dict)
    preferences: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
