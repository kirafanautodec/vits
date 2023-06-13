from typing import List, Optional
from pydantic import BaseModel

class MarkedSentence:
    content: str
    start_time: float
    end_time: float
    is_punctuation: bool


class Config:
    