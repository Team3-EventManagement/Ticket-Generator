import qrcode
import os
import uuid
import json
from datetime import datetime
from app.database import get_db

QR_CODE_DIR = "qr_codes"
if not os.path.exists(QR_CODE_DIR):
    os.makedirs(QR_CODE_DIR)

async def generate_ticket(booking_id: str, event_id: str, user_id: str):
    ticket_id = f"TICKET-{str(uuid.uuid4())[:8].upper()}"
    
    qr_data = {
        "ticket_id": ticket_id,
        "booking_id": booking_id,
        "event_id": event_id,
        "user_id": user_id
    }
    
    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(json.dumps(qr_data))
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    qr_code_filename = f"{QR_CODE_DIR}/{ticket_id}.png"
    img.save(qr_code_filename)
    
    # Store in MongoDB
    ticket_doc = {
        "_id": ticket_id,
        "booking_id": booking_id,
        "event_id": event_id,
        "user_id": user_id,
        "qr_code": qr_code_filename,
        "created_at": datetime.utcnow()
    }
    
    db = get_db()
    if db is not None:
        await db.tickets.insert_one(ticket_doc)
        print(f"Ticket {ticket_id} created and stored successfully.")
    else:
        print("Database not initialized, cannot store ticket.")
