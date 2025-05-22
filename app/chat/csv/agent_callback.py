from app.web.db.models import Message
from langchain.callbacks.base import BaseCallbackHandler
from flask import jsonify

class QueryCaptureCallbackManager(BaseCallbackHandler):

    def __init__(self, conversation_id):
        self.conversation_id = conversation_id
    
    def on_chat_model_start(self, serialized, messages, run_id, **kwargs):
        print(f"Running chat model with messages: {messages}")
        
    
    def on_llm_new_token(self, token, **kwargs):
        print(f"Running chat model with messages")
        

    def on_llm_end(self, response, run_id, **kwargs):
        print(jsonify(response))
       # Message.create(conversation_id=self.conversation_id, role='assistant', content=self.query)

    def on_llm_error(self, error, **kwargs):
        pass
        