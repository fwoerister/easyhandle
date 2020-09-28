import json
import uuid
from base64 import b64encode

from requests import get, put, delete

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
    def load_from_config(cls, config):
        return HandleClient(
            config['handle_server_url'],
            config['prefix'],
            bool(config['HTTPS_verify'])
        )

    def get_handle(self, pid: str):
        url = assemble_pid_url(self.base_url, pid)
        return get(url, header=self._get_auth_header(), verify=self.verify)

    def get_handle_by_type(self, pid, type):
        url = assemble_pid_url(self.base_url, pid)
        return get(url, params={'type': type}, header=self._get_auth_header(), verify=self.verify)

    def put_handle(self, pid_document: dict):
        url = assemble_pid_url(self.base_url, pid_document.get('handle'))

        headers = {
            'Content-Type': 'application/json'
        }
        headers.update(self._get_auth_header())

        return put(url, headers=headers, data=json.dumps(pid_document), auth=headers, verify=self.verify)

    def put_handle_for_urls(self, urls: dict):
        handle = f'{self.prefix}/{uuid.uuid1()}'
        url_entries = []

        for entry_type in urls.keys():
            url = urls[entry_type]
            url_entries.append(create_entry(1, entry_type, url))

        return self.put_handle({
            'handle': handle,
            'values': url_entries
        })

    def delete_handle(self, pid: str):
        url = assemble_pid_url(self.base_url, pid)
        return delete(url, header=self._get_auth_header(), verify=self.verify)

    def _get_auth_header(self):
        return {}


class BasicAuthHandleClient(HandleClient):
    def __init__(self, base_url, prefix, verify, username, password):
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
        credentials = b64encode(f'{self.username}:{self.password}').decode('ascii')
        return {'Authorization': f'Basic {credentials}'}
