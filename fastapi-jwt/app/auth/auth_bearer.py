from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentails: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentails:
            if not credentails.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme.",
                )
            if not self.verify_jwt(credentails.credentials):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token or expired token.",
                )
            return credentails.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code.",
            )

    def verify_jwt(self, jwt_token: str):
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwt_token)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
