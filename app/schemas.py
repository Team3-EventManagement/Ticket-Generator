from pydantic import BaseModel
from datetime import datetime

class TicketResponse(BaseModel):
    id: str
    booking_id: str
    event_id: str
    user_id: str
    qr_code: str
    created_at: datetime
