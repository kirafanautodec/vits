from typing import List, Optional
from enum import Enum, IntEnum
from pydantic import BaseModel, Field

class ErrorCode(IntEnum):
    OK = 0
    EmptyText = 100
    Unknown = 199

class Dialect(str, Enum):
    gb = 'en-gb'
    uk = gb
    us = 'en-us'

class TTSConfig(BaseModel):
    dialect: Optional[Dialect] = Field(
        Dialect.gb, description='which English dialect to use')
    slow_punctuation: Optional[float] = Field(
        4.0, description='add more stop for punctuations'
    )
    noise_scale: Optional[float] = Field(
        0.0, description='model noise'
    )
    noise_scale_w: Optional[float] = Field(
        0.0, description='model noise on duration length'
    )
    length_scale: Optional[float] = Field(
        1.0, description='duration length scale'
    )


class TTSRequest(BaseModel):
    config: Optional[TTSConfig] = None
    text: str = Field(
        description='input text to use',
        example='Hello, This is a sample text to test TTS system!'
    )

class MarkedSentence(BaseModel):
    content: str
    start_time: float
    end_time: float
    is_punctuation: bool


class TTSResponseData(BaseModel):
    marked_sentences: List[MarkedSentence]
    voice: bytes


class TTSResponse(BaseModel):
    code: ErrorCode
    msg: Optional[str] = ''
    data: Optional[TTSResponseData]
