from app.web.db import db
from .base import BaseModel
import uuid
from sqlalchemy import ForeignKey

class AnalyzeResults(BaseModel):
    __tablename__ = 'analyze_result'

    id:str = db.Column(db.String(), primary_key=True, default=lambda: str(uuid.uuid4()))
    prompt:str = db.Column(db.String())
    role:str = db.Column(db.String, default='assistant')
    content:str = db.Column(db.String())
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    document_id:str = db.Column(db.String(), db.ForeignKey('document.id'), nullable=False)
    document = db.relationship('Document', back_populates='analyze_results')

    def as_dict(self):
        return {
            "id": self.id,
            "prompt": self.prompt,
            "role": self.role,
            "content": self.content,
            "created_at": self.created_at,
            "document_id": self.document_id
        }