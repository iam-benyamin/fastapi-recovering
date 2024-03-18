from pydantic import BaseModel


class RegisterInput(BaseModel):
    username: str
    password: str  # TODO: create custom type for password with pydantic


class LoginInput(BaseModel):
    username: str
    password: str


class UpdateProfileInput(BaseModel):
    old_username: str
    username: str
