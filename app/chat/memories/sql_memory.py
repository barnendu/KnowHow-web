from typing import Sequence

from langchain.memory import ConversationBufferMemory
from langchain.schema import BaseChatMessageHistory
from langchain_core.messages import BaseMessage

from app.web.api import (
    get_messages_by_conversation_id,
    add_message_to_conversation,
)


class SqlMessageHistory(BaseChatMessageHistory):
    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id

    @property
    def messages(self) -> list[BaseMessage]:
        return get_messages_by_conversation_id(self.conversation_id)

    def add_message(self, message: BaseMessage) -> None:
        msg = message.content
        if message.type == "human":
            msg = message.content.split("Additional Instructions:")[0].strip()

        add_message_to_conversation(
            conversation_id=self.conversation_id,
            role=message.type,
            content=msg,
        )

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        for message in messages:
            self.add_message(message)

    def clear(self) -> None:
        pass


def build_memory(conversation_id: str) -> ConversationBufferMemory:
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        chat_memory=SqlMessageHistory(conversation_id=conversation_id),
    )
