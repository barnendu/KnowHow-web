from pydantic import BaseModel
from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseChatMessageHistory
import pprint
from app.web.api import (
    get_messages_by_conversation_id,
    add_message_to_conversation
)


class SqlMessageHistory(BaseChatMessageHistory, BaseModel):
    conversation_id: str

    @property
    def messages(self):
        chat_history = get_messages_by_conversation_id(self.conversation_id)
        return chat_history

    def add_message(self, message):
        msg = message.content
        if message.type == "human":
           msg = message.content.split("Additional Instructions:")[0].strip()
        return add_message_to_conversation(
            conversation_id=self.conversation_id,
            role=message.type,
            content=msg
        )

    def clear(self):
        pass


def build_memory(conversation_id):
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        chat_memory=SqlMessageHistory(
            conversation_id=conversation_id
        )
    )
