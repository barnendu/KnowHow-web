from flask import Blueprint, g, jsonify, request
from app.web.db.models import Document
from app.web.hooks import login_required, load_model, handle_file_upload
from app.web import files
from app.web.tasks.embeddings import process_document
import pprint

bp = Blueprint('documents', __name__, url_prefix='/api/pdfs')


@bp.route('/', methods=['GET'])
@login_required
def list():
    page = request.args.get('page')
    documents = Document.where(user_id=g.user.id)
    if documents is None:
        return jsonify(None)
    return Document.as_dicts(documents)


@bp.route('/', methods=['POST'])
@login_required
@handle_file_upload
def upload_file(file_id, file_path, file_name, file_size, file_extension):
    res, status_code = files.upload(file_path, file_name)

    if status_code >= 400:
        return res, status_code
    doc = Document.create(id=file_id, name=file_name, document_ext= file_extension, user_id=g.user.id)
    try:
        process_document(doc.id,file_extension)
    except Exception as e:
        print(e)
    return doc.as_dict()

@bp.route("/<string:document_id>", methods=['GET'])
@login_required
@load_model(Document)
def show(document):
    return jsonify(
        {
            "pdf": document.as_dict(),
            "download_url": files.create_download_url(document.id),
        }
    )