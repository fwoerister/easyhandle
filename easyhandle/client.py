import base64
import json
import uuid

import requests
from requests import Response

from easyhandle.util import assemble_pid_url, create_entry


class HandleClient:
    '''
    Base class for accessing handle services.
    '''

    def __init__(self, base_url, prefix, verify=True):
        self.base_url = base_url
        self.prefix = prefix
        self.verify = verify

    @classmethod
    def load_from_config(cls, config: dict):
        return HandleClient(
            config['handle_server_url'],
            config['prefix'],
            bool(config['HTTPS_verify'])
        )

    def get_handle(self, pid: str) -> Response:
        url = assemble_pid_url(self.base_url, pid)
        return requests.get(url, header=self._get_auth_header(), verify=self.verify)

    def get_handle_by_type(self, pid: str, type: str) -> Response:
        url = assemble_pid_url(self.base_url, pid)
        return requests.get(url, params={'type': type}, header=self._get_auth_header(), verify=self.verify)

    def put_handle(self, pid_document: dict) -> Response:
        url = assemble_pid_url(self.base_url, pid_document.get('handle'))

        headers = {
            'Content-Type': 'application/json'
        }
        headers.update(self._get_auth_header())

        return requests.put(url, headers=headers, data=json.dumps(pid_document), auth=headers, verify=self.verify)

    def put_handle_for_urls(self, urls: dict) -> Response:
        handle = f'{self.prefix}/{uuid.uuid1()}'
        url_entries = []

        for entry_type in urls.keys():
            url = urls[entry_type]
            url_entries.append(create_entry(1, entry_type, url))

        return self.put_handle({
            'handle': handle,
            'values': url_entries
        })

    def delete_handle(self, pid: str) -> Response:
        url = assemble_pid_url(self.base_url, pid)
        return requests.delete(url, header=self._get_auth_header(), verify=self.verify)

    def _get_auth_header(self) -> dict:
        return {}


class BasicAuthHandleClient(HandleClient):
    '''
        Handle Client implementation that uses `BasicAuth` for authentication
    '''

    def __init__(self, base_url: str, prefix: str, verify: bool, username:str, password:str):
        super().__init__(base_url, prefix, verify)
        self.username = username
        self.password = password

    @classmethod
    def load_from_config(cls, config):
        return BasicAuthHandleClient(
            config['handle_server_url'],
            config['prefix'],
            bool(config['HTTPS_verify']),
            config['username'],
            config['password']
        )

    def _get_auth_header(self):
        credentials = base64.b64encode(f'{self.username}:{self.password}'.encode('utf-8')).decode('ascii')
        return {'Authorization': f'Basic {credentials}'}
