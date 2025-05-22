import os
from flask import Blueprint, send_from_directory, current_app

bp = Blueprint('client', __name__)

@bp.route('/<path:path>')
@bp.route('/', defaults={'path': ''})
def catch_all(path):
    if path !="" and os.path.exists(os.path.join(current_app.static_folder, path)):
        return send_from_directory(current_app.static_folder, path)
    else:
        return send_from_directory(current_app.static_folder, 'index.html')