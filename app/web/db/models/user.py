from .base import BaseModel
import uuid
from app.web.db import db



class User(BaseModel):
    id: str = db.Column(
        db.String(), primary_key=True, default= lambda : str(uuid.uuid4())
        )
    email: str = db.Column(db.String(), nullable=False, unique=True)
    password: str = db.Column(db.String(), nullable=False)  
    documents = db.relationship('Document', back_populates='user')
    conversations = db.relationship('Conversation', back_populates='user')

    def as_dict(self):
        return {"id": self.id, "email": self.email}