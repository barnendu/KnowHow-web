import uuid
from app.web.db import db
from .base import BaseModel



class Document(BaseModel):
    id: str = db.Column(db.String(), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: str = db.Column(db.String(), nullable=False)
    document_ext: str = db.Column(db.String(), nullable=False)
    user_id: str = db.Column(db.String(), db.ForeignKey("user.id"), nullable=False)
    uploaded_on = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
    user = db.relationship("User", back_populates="documents")

    conversations = db.relationship("Conversation", 
                                   back_populates="document",
                                   order_by="desc(Conversation.created_on)"
                                   )
    analyze_results = db.relationship("AnalyzeResults", back_populates="document")
    
    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name, 
            "user_id": self.user_id,
            "uploaded_on": self.uploaded_on,
            "document_ext": self.document_ext,
            }