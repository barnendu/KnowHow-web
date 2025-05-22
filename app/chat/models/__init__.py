from pydantic import BaseModel, Extra

class Metadata(BaseModel, extra=Extra.allow):
    conversation_id: str
    user_id: str
    document_id: str

class ChatArgs(BaseModel, extra=Extra.allow):
    conversation_id: str
    document_id: list[str]
    metadata: Metadata
    streaming: bool
