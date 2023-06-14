import os
import sys

from fastapi import FastAPI

from tts_service import TTSService
from schema import TTSResponse, TTSRequest, ErrorCode

app = FastAPI()

@app.get('/')
async def root():
    return 'OK!'

tts_service = TTSService()
@app.post("/tts")
async def tts(req: TTSRequest) -> TTSResponse:
    try:
        return tts_service.run(req)
    except Exception as err:
        return TTSResponse(code=ErrorCode.Unknown, msg=str(err))
