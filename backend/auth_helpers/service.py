from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import uuid

from .database import supabase_db
from .security import hash_user_password, check_password_match, generate_jwt_token, decode_jwt_token

# create pydantic models
class RegistrationData(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    email_address: EmailStr
    department_name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=6)

class LoginData(BaseModel):
    email_address: EmailStr
    password: str

class UserInfo(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    email_address: EmailStr
    department_name: str
    created_at: Optional[datetime] = None

class UpdateUserProfile(BaseModel):
    first_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    email_address: Optional[EmailStr] = None
    department_name: Optional[str] = Field(default=None, min_length=1, max_length=100)

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserInfo

# registration and login service class
class AuthService:
    
    @staticmethod
    def register_new_user(registration_data: RegistrationData):
        """Register a new user"""
        
        # Check if the user with this specific email already exists
        existing_user = supabase_db.find_user_by_email(registration_data.email_address)
        if existing_user is not None:
            raise HTTPException(status_code=400, detail="This email is already registered")
        
        # hash the password | security metrics
        hashed_password = hash_user_password(registration_data.password)
        
        # prepare user data for database
        new_user_data = {
            "fname": registration_data.first_name.strip(),
            "lname": registration_data.last_name.strip(),
            "email": registration_data.email_address.lower().strip(),
            "department": registration_data.department_name.strip(),
            "password_hash": hashed_password,
            "created_at": datetime.utcnow().isoformat()
        }
        
        # Save user record to supabase database
        saved_user = supabase_db.insert_new_user(new_user_data)
        if saved_user is None:
            raise HTTPException(status_code=500, detail="Failed to create user account")
        
        # generate JWT token
        jwt_token = generate_jwt_token(registration_data.email_address)
        
        # return the response
        user_info = UserInfo(
            user_id=str(saved_user["id"]),
            first_name=saved_user["fname"],
            last_name=saved_user["lname"],
            email_address=saved_user["email"],
            department_name=saved_user["department"],
            created_at=saved_user.get("created_at")
        )
        
        return LoginResponse(
            access_token=jwt_token,
            user=user_info
        )
    
    @staticmethod
    def login_user(login_data: LoginData):
        """Login a user"""
        
        # find user by email before login
        user = supabase_db.find_user_by_email(login_data.email_address)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Check that password is correct by comparing the hash 
        stored_password_hash = user.get("password_hash", "")
        if not check_password_match(login_data.password, stored_password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # Generate JWT token for logged in user
        jwt_token = generate_jwt_token(login_data.email_address)
        
        # Return response
        user_info = UserInfo(
            user_id=str(user["id"]),
            first_name=user["fname"],
            last_name=user["lname"],
            email_address=user["email"],
            department_name=user["department"],
            created_at=user.get("created_at")
        )
        
        return LoginResponse(
            access_token=jwt_token,
            user=user_info
        )
    
    @staticmethod
    def get_current_user_info(jwt_token):
        """Get current user info from token"""
        
        # decode token
        token_data = decode_jwt_token(jwt_token)
        if token_data is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # get email from token
        user_email = token_data.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # find user in database
        user = supabase_db.find_user_by_email(user_email)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        # Return user info
        return UserInfo(
            user_id=str(user["id"]),
            first_name=user["fname"],
            last_name=user["lname"],
            email_address=user["email"],
            department_name=user["department"],
            created_at=user.get("created_at")
        )

    @staticmethod
    def update_current_user_profile(jwt_token, profile_update: UpdateUserProfile):
        """Update the authenticated user's profile fields in the database."""
        token_data = decode_jwt_token(jwt_token)
        if token_data is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_email = token_data.get("sub")
        if user_email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        current_user = supabase_db.find_user_by_email(user_email)
        if current_user is None:
            raise HTTPException(status_code=401, detail="User not found")

        updates = {}
        if profile_update.first_name is not None:
            first_name = profile_update.first_name.strip()
            if first_name:
                updates["fname"] = first_name
        if profile_update.last_name is not None:
            last_name = profile_update.last_name.strip()
            if last_name:
                updates["lname"] = last_name
        if profile_update.department_name is not None:
            department_name = profile_update.department_name.strip()
            if department_name:
                updates["department"] = department_name
        if profile_update.email_address is not None:
            normalized_email = str(profile_update.email_address).lower().strip()
            if normalized_email:
                if normalized_email != current_user.get("email"):
                    existing_user = supabase_db.find_user_by_email(normalized_email)
                    if existing_user is not None:
                        raise HTTPException(status_code=400, detail="This email is already registered")
                    updates["email"] = normalized_email

        if not updates:
            raise HTTPException(status_code=400, detail="No profile changes provided")

        updated_user = supabase_db.update_user_profile(current_user["id"], updates)
        if updated_user is None:
            raise HTTPException(status_code=500, detail="Failed to update profile")

        return UserInfo(
            user_id=str(updated_user["id"]),
            first_name=updated_user.get("fname") or current_user["fname"],
            last_name=updated_user.get("lname") or current_user["lname"],
            email_address=updated_user.get("email") or current_user["email"],
            department_name=updated_user.get("department") or current_user["department"],
            created_at=updated_user.get("created_at") or current_user.get("created_at")
        )


