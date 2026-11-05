from datetime import datetime

from app.extensions import db


class Institution(db.Model):
    __tablename__ = "institutions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    url = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(100))  # e.g. regulator, exchange, unit_trust, broker
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Institution {self.name}>"
