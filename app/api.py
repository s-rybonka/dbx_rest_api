from flask import Blueprint
from flask import jsonify
from flask import request

from app.responses import FileResponse
from app.schemas import SearchQuerySchema
from app.services import DBoxApiService
from config import Config

bp = Blueprint('d-box', __name__, url_prefix='/api')


@bp.route('/%s-items' % bp.name, methods=['GET'])
def dbx_items_api_view():
    """
    Get Dropbox item list, include folders and files.
    Query params: [path,]
    Api call example: domain/api/d-box-items?path=/bookmarks
    :return: {
    "dbx_items": [
        {
          "id": "id:zqmqAdvBreAAAAAAAAAAQw",
          "name": "bookmarks",
          "path_lower": "/bookmarks",
          "type": "folder"
        },
        ...
      ],
    }
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
    return jsonify({'dbx_items': object_list})


@bp.route('/%s-search' % bp.name)
def d_box_search_api_view():
    """
    Make recursive search through dropbox items.
    Query params: [path, token].
    Api call example: domain/api/d-box-search?token=bookmarks
    :return: [
      {
        "id": "id:zqmqAdvBreAAAAAAAAAAQw",
        "name": "bookmarks",
        "path_lower": "/bookmarks",
        "type": "folder"
       },
       ...
     ]
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
    return jsonify(data_to_response)


@bp.route('/%s-item-download' % bp.name)
def d_box_item_download_api_view():
    """
    Download Dropbox items, folders or files.
    Folder can be loaded like zip.
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
