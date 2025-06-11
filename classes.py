from dataclasses import dataclass
@dataclass
class Article:
    title: str
    description: str
    url: str
    
@dataclass
class AudioResponse:
    i: int
    gs: str
    ps: str
    audio: str