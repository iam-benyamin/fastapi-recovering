from uuid import UUID

from pydantic import BaseModel


class RegisterOutput(BaseModel):
    id: UUID
    username: str
