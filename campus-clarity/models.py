from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Message(db.Model):
    """
    Ek row = ek processed campus update (event/deadline/notice waghera)
    AI processing ke baad yahan save hota hai
    """
    id = db.Column(db.Integer, primary_key=True)

    # Original raw text jo user ne paste kiya tha
    raw_text = db.Column(db.Text, nullable=False)

    # AI ne jo nikala - structured fields
    title = db.Column(db.String(200))              # short title, jaise "TCS NQT Registration"
    category = db.Column(db.String(50))             # deadline / event / cancellation / opportunity
    event_date = db.Column(db.String(50))            # jaise "16 Sept" (string rakha hai simplicity ke liye)
    urgency = db.Column(db.String(20), default="soon")  # now / soon / later
    seats_limited = db.Column(db.Boolean, default=False)
    is_cancelled = db.Column(db.Boolean, default=False)
    missing_info = db.Column(db.Boolean, default=False)  # agar AI ko info incomplete lagi

    # Duplicate/conflict tracking
    duplicate_count = db.Column(db.Integer, default=1)   # kitne messages isi topic pe milke bane
    has_conflict = db.Column(db.Boolean, default=False)
    conflict_note = db.Column(db.String(300))             # kis se clash ho raha hai

    # CRUD ke liye - student khud control kar sake
    status = db.Column(db.String(20), default="pending")  # pending / done / ignored

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Message {self.id}: {self.title}>"
