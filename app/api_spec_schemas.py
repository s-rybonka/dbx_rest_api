
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "DBX Scrapper API",
        "description": "REST API client for work with Dropbox.",
        "contact": {
            "responsibleDeveloper": "Stanislav Rybonka",
            "email": "stanislav.rybonka@gmail.com",
        },
        "version": "0.0.1"
    },
    "schemes": [
        "http",
        "https"
    ],
    "operationId": "getSwaggerRootSchema"
}

dbx_item_base_structure = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "string",
                    },
                    "name": {
                        "type": "string"
                    },
                    "size": {
                        "type": "string"
                    },
                    "path_lower": {
                        "type": "string"
                    },
                    "client_modified": {
                        "type": "string"
                    },
                    "server_modified": {
                        "type": "string"
                    },
                }
            }
        }
    }
}

d_box_items_api_spec = {

    "parameters": [
        {
            "name": "path",
            "in": "query",
            "type": "string",
            "required": False,
        },
        {
            "name": "ordering",
            "in": "query",
            "type": "string",
            "required": False,
        }
    ],
    "definitions": {
        "Dbx-Item": dbx_item_base_structure,
    },
    "responses": {
        "200": {
            "description": "Get a list of Dropbox items. [Root dir]",
            "content": {
                "application/json": {},
            },
            "schema": {
                "$ref": "#/definitions/Dbx-Item"
            }
        },
        "400": {
            "description": "Bad request.",
            "content": {
                "application/json": {},
            },
            "schema": {
                "type": "object",
                "properties": {
                    "errors": {
                        "type": "string"
                    }
                }

            }
        }
    }
}

d_box_search_api_spec = {

    "parameters": [
        {
            "name": "path",
            "in": "query",
            "type": "string",
            "required": False,
        },
        {
            "name": "token",
            "in": "query",
            "type": "string",
            "required": False,
        }
    ],
    "definitions": {
        "Dbx-Item": dbx_item_base_structure,
    },
    "responses": {
        "200": {
            "description": "Make recursive search through Dropbox folders.",
            "content": {
                "application/json": {},
            },
            "schema": {
                "$ref": "#/definitions/Dbx-Item"
            }
        },
        "400": {
            "description": "Bad request.",
            "content": {
                "application/json": {},
            },
            "schema": {
                "type": "object",
                "properties": {
                    "errors": {
                        "type": "string"
                    }
                }

            }
        }
    }
}

d_box_item_download_api_spec = {

    "parameters": [
        {
            "name": "path",
            "in": "query",
            "type": "string",
            "required": True,
        },
        {
            "name": "content_type",
            "in": "query",
            "type": "string",
            "required": True,
        }
    ],
    "definitions": {
        "Dbx-Item": dbx_item_base_structure,
    },
    "responses": {
        "200": {
            "description": "Download DBX items. Folder - zip. File - attached object.",
            "content": {
                "application/octet-stream": [],
            },
        },
        "400": {
            "description": "Bad request.",
            "content": {
                "application/json": {},
            },
            "schema": {
                "type": "object",
                "properties": {
                    "errors": {
                        "type": "string"
                    }
                }

            }
        }
    }
}
