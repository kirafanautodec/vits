import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tts_service import TTSService
from schema import TTSResponse, TTSRequest, ErrorCode

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
