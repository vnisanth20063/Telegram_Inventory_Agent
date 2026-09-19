from pydantic import BaseModel


class MessageCreate(BaseModel):
    phone_number: str
    message: str
    sender: str