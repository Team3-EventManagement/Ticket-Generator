from fastapi import APIRouter, HTTPException
from typing import List
from app.database import get_db
from app.schemas import TicketResponse

router = APIRouter()

@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: str):
    db = get_db()
    ticket = await db.tickets.find_one({"_id": ticket_id})
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    ticket['id'] = ticket.pop('_id')
    return ticket

@router.get("/user/{user_id}", response_model=List[TicketResponse])
async def get_user_tickets(user_id: str):
    db = get_db()
    cursor = db.tickets.find({"user_id": user_id})
    tickets = await cursor.to_list(length=100)
    
    result = []
    for t in tickets:
        t['id'] = t.pop('_id')
        result.append(t)
    return result

@router.get("/verify/{ticket_id}")
async def verify_ticket(ticket_id: str):
    db = get_db()
    ticket = await db.tickets.find_one({"_id": ticket_id})
    if not ticket:
        return {"valid": False, "message": "Ticket not found or invalid"}
        
    return {"valid": True, "ticket_id": ticket_id, "event_id": ticket.get("event_id")}
