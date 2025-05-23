from typing import Dict, List
from langchain.schema.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from app.web.db import db
from app.web.db.models import Message
from app.web.db.models import Conversation


def get_messages_by_conversation_id(
        conversation_id: str
) -> AIMessage | HumanMessage | SystemMessage:
    messages = (
        db.session.query(Message)
        .filter_by(conversation_id=conversation_id)
        .order_by(Message.created_on.desc())

    )
    return [message.as_lc_message() for message in messages]




def add_message_to_conversation(
        conversation_id: str, role: str, content: str
) -> Message:
    return Message.create(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )


def set_conversation_components(
        conversation_id: str,
        llm: str,
        retriever: str,
        memory: str
) -> None:
    conversation = Conversation.find_by(id=conversation_id)
    conversation.update(llm=llm, retriever=retriever, memory=memory)


def get_conversation_components(
        conversation_id: str
) -> Dict[str, str]:
    conversation = Conversation.find_by(id=conversation_id)
    return {
        "llm": conversation.llm,
        "retriever": conversation.retriever,
        "memory": conversation.memory
    }
