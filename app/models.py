from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Ticket(BaseModel):
    id: str = Field(alias="_id")
    booking_id: str
    event_id: str
    user_id: str
    qr_code: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
