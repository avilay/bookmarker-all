from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class ToRead:
    is_important: bool = False
    is_urgent: bool = False


@dataclass
class Note:
    created_at: datetime
    # contents: List[str] = field(default_factory=list)
    contents: str


@dataclass
class Bookmark:
    id: int = 0
    title: str = ""
    url: str = ""
    to_read: Optional[ToRead] = None
    notes: List[Note] = field(default_factory=list)
