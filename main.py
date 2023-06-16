import os
import sys

from typing import Optional

from fastapi import FastAPI, Header
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from tts_service import TTSService
from user_service import UserService
from schema import TTSResponse, TTSRequest, UserLoginResponse, UserLoginResponseData, UserLoginRequest, ErrorCode

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tts_service = TTSService()
user_service = UserService()

@app.post("/tts/syn")
async def tts(req: TTSRequest, authorization: Optional[str] = Header(...)) -> TTSResponse:
    try:
        if user_service.check_token(authorization):
            return tts_service.syn(req)
        else:
            return TTSResponse(code=ErrorCode.InvalidLogin, msg='You login is expired!')
    except Exception as err:
        return TTSResponse(code=ErrorCode.Unknown, msg=str(err))

@app.post("/tts/login")
async def tts(req: UserLoginRequest) -> UserLoginResponse:
    try:
        return user_service.login(req)
    except Exception as err:
        return UserLoginResponse(code=ErrorCode.Unknown, msg=str(err))

app.mount('', StaticFiles(directory='vits-webui/dist/', html=True), name='static')