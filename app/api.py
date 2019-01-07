from flasgger import swag_from
from flask import Blueprint
from flask import jsonify
from flask import request

from app import api_spec_schemas as doc_schemas
from app.responses import FileResponse
from app.schemas import SearchQuerySchema
from app.services import DBoxApiService
from config import Config

bp = Blueprint('d-box', __name__, url_prefix='/api')


@bp.route('/%s-items' % bp.name, methods=['GET'])
@swag_from(doc_schemas.d_box_items_api_spec)
def dbx_items_api_view():
    """
    Get Dropbox item list, include folders and files.
    """
    dbx = DBoxApiService(access_token=Config.DROPBOX_ACCESS_TOKEN)
    parse_query_errors = SearchQuerySchema().validate(data=request.args)
    if parse_query_errors:
        return jsonify({
            'status_code': 400,
            'errors': parse_query_errors
        })
    object_list = dbx.get_d_box_item_list(**{
        'path': request.args.get('path', ''),
        'ordering': request.args.get('ordering', '')
    })
    return jsonify({'results': object_list})


@bp.route('/%s-search' % bp.name)
@swag_from(doc_schemas.d_box_search_api_spec)
def d_box_search_api_view():
    """
    Make recursive search through Dropbox items.
    """
    dbx = DBoxApiService(access_token=Config.DROPBOX_ACCESS_TOKEN)
    parse_query_errors = SearchQuerySchema().validate(data=request.args)
    if parse_query_errors:
        return jsonify(parse_query_errors)
    data_to_response = dbx.d_box_files_search(
        **{
            'path': request.args.get('path', ''),
            'token': request.args.get('token', '')
        }
    )
    return jsonify({'results': data_to_response})


@bp.route('/%s-item-download' % bp.name)
@swag_from(doc_schemas.d_box_item_download_api_spec)
def d_box_item_download_api_view():
    """
    Download Dropbox items, folders or files.
    Folder can be loaded like zip.
    File like attached object.
    Api call examples: [
        domain/api/d-box-item-download?content_type=zip&path=/bookmarks,
        domain/api/d-box-item-download?content_type=file&path=/bookmark_1.1.html,
    ]
    :return: Attached file or binary, will be recognized by browser.
    """
    dbx = DBoxApiService(access_token=Config.DROPBOX_ACCESS_TOKEN)
    parse_query_errors = SearchQuerySchema().validate(data=request.args)
    if parse_query_errors:
        return jsonify(parse_query_errors)
    file_data = dbx.download_d_box_item(**{
        'path': request.args.get('path'),
        'content_type': request.args.get('content_type')
    })
    if file_data and file_data.get('filename'):
        response = FileResponse(
            response=file_data.get('file')
        )
        response.set_headers(file_data.get('filename'))
        return response
    elif file_data.get('errors'):
        return jsonify(file_data.get('errors'))
