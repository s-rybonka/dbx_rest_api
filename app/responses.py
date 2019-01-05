from flask import Response


class FileResponse(Response):
    default_mimetype = 'application/octet-stream'

    def set_headers(self, filename):
        self.headers['Content-Disposition'] = 'attachment; filename={}'.format(filename)