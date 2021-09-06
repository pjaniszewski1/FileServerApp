from distutils.util import strtobool

from server.file_service import FileService, FileServiceSigned
from aiohttp import web
import json


class Handler:
    def __init__(self, path: str) -> None:
        self.file_service = FileService(path=path)
        self.file_service_signed = FileServiceSigned(path=path)

    async def handle(self, request: web.Request, *args, **kwargs) -> web.Response:
        return web.json_response(data={
            'status': 'success'
        })

    async def get_files(self, request: web.Request, *args, **kwargs) -> web.Response:
        return web.json_response(data={
            'status': 'success',
            'data': self.file_service.get_files()
        })

    async def get_file_info(self, request: web.Request, *args, **kwargs) -> web.Response:
        try:
            filename = request.rel_url.query['filename']
            is_signed = request.rel_url.query['is_signed']
            assert is_signed in ['true', 'false'], 'Is_signed is invalid'
            is_signed = strtobool(is_signed)

            if is_signed:
                file_service = self.file_service_signed
            else:
                file_service = self.file_service

            result = await file_service.get_file_data_async(filename)
            result['size'] = '{} bytes'.format(result['size'])

            return web.json_response(data={
                'status': 'success',
                'data': result
            })

        except (AssertionError, ValueError) as err:
            raise web.HTTPBadRequest(text='{}'.format(err))

        except KeyError as err:
            raise web.HTTPBadRequest(text='Parameter {} is not set'.format(err))

    async def create_file(self, request: web.Request, *args, **kwargs) -> web.Response:
        result = ''
        stream = request.content

        while not stream.at_eof():
            line = await stream.read()
            result += line.decode('utf-8')

        try:

            data = json.loads(result)
            is_signed = bool(strtobool(data.get('is_signed', 'False')))

            if is_signed:
                file_service = self.file_service_signed
            else:
                file_service = self.file_service

            result = await file_service.create_file(data.get('content'), data.get('security_level'))
            result['size'] = '{} bytes'.format(result['size'])

            return web.json_response(data={
                'status': 'success',
                'data': result
            })
        except (AssertionError, ValueError) as err:
            raise web.HTTPBadRequest(text='{}'.format(err))

    async def delete_file(self, request: web.Request, *args, **kwargs) -> web.Response:
        filename = request.match_info['filename']

        try:
            return web.json_response(data={
                'status': 'success',
                'message': 'File {} is successfully deleted'.format(self.file_service.delete_file(filename))
            })
        except AssertionError as err:
            raise web.HTTPBadRequest(text='{}'.format(err))

    async def change_file_dir(self, request: web.Request, *args, **kwargs) -> web.Response:
        result = ''
        stream = request.content

        while not stream.at_eof():
            line = await stream.read()
            result += line.decode('utf-8')

        try:
            data = json.loads(result)
            path = data.get('path')
            assert path, 'Directory path is not set'

            self.file_service.path = path
            self.file_service_signed.path = path

            return web.json_response(data={
                'status': 'success',
                'message': 'You successfully changed working directory path. New path is {}'.format(path)
            })
        except (AssertionError, ValueError) as err:
            raise web.HTTPBadRequest(text='{}'.format(err))
