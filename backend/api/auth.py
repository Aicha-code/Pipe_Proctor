from fastapi import APIRouter, Header, HTTPException
from typing import Optional

from auth_helpers import AuthService
from auth_helpers.service import RegistrationData, LoginData, LoginResponse, UserInfo

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register", response_model=LoginResponse)
def register_new_user(registration_data: RegistrationData):
    """Register a new user account"""
    return AuthService.register_new_user(registration_data)

@auth_router.post("/login", response_model=LoginResponse)
def login_user(login_data: LoginData):
    """login to your account"""
    return AuthService.login_user(login_data)

@auth_router.get("/me", response_model=UserInfo)
def get_my_profile(authorization: Optional[str] = Header(None)):
    """Get your profile information"""
    
    ## check if authorization header exists
    
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    # check if it is a Bearer token
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    # extract token from authorization bearer
    jwt_token = authorization.split(" ")[1]
    
    # get user info
    return AuthService.get_current_user_info(jwt_token)