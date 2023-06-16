import time
import jwt
from datetime import datetime, timedelta, timezone
from schema import UserLoginRequest, UserLoginResponse, UserLoginResponseData, ErrorCode


class UserService:
    _SECRET = 'wervghni8w34vgbhyi8o9p3tbyngtbhn8opw4v5gthny89seyhno95tbn89p'
    
    def __init__(self):
        pass

    def check_token(self, authorization) -> bool:
        if (len(authorization) < 8):
            return False

        if authorization[:7] != 'Bearer ':
            return False

        token = authorization[7:]
        try:
            result = jwt.decode(token, key=self._SECRET, algorithms=['HS256'])
            if result is None or result['exp'] is None:
                return False
            exp = result['exp']
            return exp >= datetime.now(timezone.utc).timestamp()
        except Exception:
            return False

    def login(self, request: UserLoginRequest) -> UserLoginResponse:
        if (request.name != 'admini'):
            return UserLoginResponse(code=ErrorCode.InvalidLogin, msg='You are not allowed to use this system!')
        if (request.password != 'c6ad2eda943e099476bfc1f7ec0045e3'):
            return UserLoginResponse(code=ErrorCode.InvalidLogin, msg='You are not allowed to use this system!')

        token = jwt.encode(dict(exp=datetime.now(timezone.utc) + timedelta(days=1)), key=self._SECRET, algorithm='HS256')
        print(token)
        return UserLoginResponse(code=ErrorCode.OK, msg='', data=UserLoginResponseData(token=token))
