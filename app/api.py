from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request
from app.schemas import SearchQuerySchema
from app.services import DBoxApiService
from app.responses import FileResponse

bp = Blueprint('d-box', __name__, url_prefix='/api')

access_token = ''


@bp.route('/dbx-items', methods=['GET'])
def dbx_items_api_view():
    dbx = DBoxApiService(access_token=access_token)
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
    print(request.args.get('path', ''))
    return jsonify({'dbx_items': object_list})


@bp.route('/%s-search' % bp.name)
def d_box_search_api_view():
    dbx = DBoxApiService(access_token=access_token)
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
    dbx = DBoxApiService(access_token=access_token)
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



