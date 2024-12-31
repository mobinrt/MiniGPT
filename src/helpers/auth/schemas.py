from pydantic import BaseModel, Field, EmailStr

class AccessTokenDisplay(BaseModel):
    access_token: str
    token_type: str

    model_config = {
        'from_attributes': True
    }


class TokenDisplay(AccessTokenDisplay):
    refresh_token: str
    
    model_config = {
        'from_attributes': True
    }    

    
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., pattern=r"^0\d{9}$") 