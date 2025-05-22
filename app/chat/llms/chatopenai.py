from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama, Bedrock


def build_llm(chat_args):
       return ChatOpenAI(model="gpt-4o", streaming=True, temperature=0.6)
      #  return Ollama(model="llama3:8b", temperature=0.6)
    # return Bedrock(
    #     model_id="meta.llama3-8b-instruct-v1:0",
    #     client=None,  # Uses default AWS credentials
    #     model_kwargs={
    #         "max_gen_len": 1024,
    #         "temperature": 0.7,
    #         "top_p": 0.9,
    #     },
    #     streaming = True,
    # )
