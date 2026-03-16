from pydantic import BaseModel

class UserCreate(BaseModel):
    tenant_id: int
    email: str
    phone: str
    password: str
