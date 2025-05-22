from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from app.chat.models import ChatArgs
from app.chat.csv.agent_callback import QueryCaptureCallbackManager
from langchain.agents import AgentType
from langchain.callbacks.manager import CallbackManager


def build_csv_agent(user_id:str, document_name:str, chat_args:ChatArgs):
    engine = create_engine(f"sqlite:///instance/{user_id}_{document_name.split('.')[0]}.db")
    db = SQLDatabase(engine=engine)
    print(db.get_usable_table_names())
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    handlers =[QueryCaptureCallbackManager(chat_args.conversation_id)]
    callback_manager = CallbackManager(handlers)
    return create_sql_agent(llm, db=db, callback_manager=callback_manager, agent_type=AgentType.OPENAI_FUNCTIONS, verbose=True)
