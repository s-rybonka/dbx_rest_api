from itertools import chain

from dropbox import Dropbox
from dropbox.files import FileMetadata
from dropbox.files import FolderMetadata

from app.decorators import d_box_catch_exceptions
from app.schemas import DBoxItemSchema
from app.utils import sort_items_by_name
from config import Config


class DBoxApiService(object):
    def __init__(self, access_token):
        self.access_token = access_token

    @d_box_catch_exceptions
    def activate_d_box_interface(self):
        return Dropbox(self.access_token)

    @d_box_catch_exceptions
    def get_d_box_item_list(self, **query_params):
        dbx = self.activate_d_box_interface()
        d_box_entries = dbx.files_list_folder(
            query_params.get('path')).entries
        return self.set_dbx_items_type(d_box_entries, query_params)

    @d_box_catch_exceptions
    def d_box_files_search(self, **query_params):
        dbx = self.activate_d_box_interface()
        searched_items = dbx.files_search(
            path=query_params.get('path'),
            query=query_params.get('token')
        ).matches
        return self.set_dbx_items_type([
            s_item.metadata for s_item in searched_items
        ], query_params)

    @d_box_catch_exceptions
    def download_d_box_item(self, **query_params):
        dbx = self.activate_d_box_interface()
        content_type = query_params.get('content_type', '')
        path = query_params.get('path', '')
        call_backs = {
            'content_type_file': dbx.files_download,
            'content_type_zip': dbx.files_download_zip,
        }
        metadata, file = call_backs['content_type_{}'.format(content_type)](
            path=path
        )
        name = metadata.metadata.name + '.zip' if 'zip' in content_type else metadata.name
        return {'file': file.content, 'filename': name}

    def set_dbx_items_type(self, raw_dbx_items, query_params):
        schema = DBoxItemSchema()
        folders = []
        files = []
        for d_box_item in raw_dbx_items:
            d_box_item_to_dict = schema.dump(d_box_item).data
            if isinstance(d_box_item, FolderMetadata):
                d_box_item_to_dict['type'] = 'folder'
                d_box_item_to_dict = self.build_download_item_link(
                    d_box_item_to_dict,
                    'zip'
                )
                folders.append(d_box_item_to_dict)
            elif isinstance(d_box_item, FileMetadata):
                d_box_item_to_dict['type'] = 'file'
                d_box_item_to_dict = self.build_download_item_link(
                    d_box_item_to_dict,
                    'file'
                )
                files.append(d_box_item_to_dict)
        sorted_data = list(
            chain(
                sort_items_by_name(folders, **query_params),
                sort_items_by_name(files, **query_params)
            )
        )
        return sorted_data

    @classmethod
    def build_download_item_link(cls, dbx_item, content_type):
        dbx_item['download_link'] = '{}://{}/api/d-box-item-download?content_type={}&path={}'.format(
            Config.PROTOCOL,
            Config.DOMAIN,
            content_type,
            dbx_item.get('path_lower')
        )
        return dbx_item

