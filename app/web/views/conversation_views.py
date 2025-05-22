import pprint
import asyncio
from flask import Blueprint, g, request, Response, jsonify, stream_with_context
from app.web.hooks import login_required, load_model
from app.web.db.models import Document, Conversation, AnalyzeResults
from app.chat import build_chat, ChatArgs
from app.chat.csv import build_csv_agent, build_query



bp = Blueprint('conversation', __name__, url_prefix='/api/conversations')

@bp.route("/", methods=["GET"])
@login_required
def list_conversations():
    document_id= request.args.get("document_id")
    conversations = Conversation.where(document_id=document_id)
    return [c.as_dict() for c in conversations]


@bp.route("/", methods=["POST"])
@login_required
def create_conversation():
    document_id= request.args.get("document_id")
    conversation = Conversation.create(user_id=g.user.id, document_id=document_id)
    return conversation.as_dict()


@bp.route("/<string:conversation_id>/messages", methods=["POST"])
@login_required
@load_model(Conversation)
def create_message(conversation):
    input = request.json.get("input")
    docList = request.json.get("docList")
    template = request.json.get("template")
    streaming = request.args.get("stream", False)
    query = f"{input} Additional Instructions: {template}"
    document = conversation.document
    docIdList = []
    if not docList:
          docIdList.append(document.id)
    else:
        docIdList = docList.copy()
    char_args = ChatArgs(
        conversation_id=conversation.id,
        document_id=docIdList,
        streaming=streaming,
        metadata={
            "conversation_id": conversation.id,
            "document_id": document.id,
            "user_id": g.user.id
        }
    )
    if not document.document_ext == "csv":
        chat = build_chat(char_args)
        if not chat:
            return "Chat not yet implemented!"
        
        if streaming:
            return Response(
                stream_with_context(chat.stream(query)), mimetype="text/event-stream"
            )
        else:
            return jsonify({"role":"assistant", "content": chat.run(query)})
    else:
       csv_agent = build_csv_agent(g.user.id, document.name, char_args)
       response = csv_agent.run(build_query(input))
       return response


