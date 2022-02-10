from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jwtoken import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    authorization: str = request.cookies.get("access_token")
    scheme, param = get_authorization_scheme_param(authorization)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if authorization:
        if not authorization or scheme.lower() != "bearer":
            raise credentials_exception
        token = param

    return verify_token(token, credentials_exception)
