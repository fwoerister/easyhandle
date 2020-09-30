import base64
import json
import uuid

import requests

from easyhandle.util import assemble_pid_url, create_entry


class HandleClient(object):
    '''
    Base class for accessing handle services.
    '''

    def __init__(self, base_url, prefix, https_verify=True):
        self.base_url = base_url
        self.prefix = prefix
        self.verify = https_verify

    @classmethod
    def load_from_config(cls, config):
        return HandleClient(
            config['handle_server_url'],
            config['prefix'],
            bool(config['HTTPS_verify'])
        )

    def get_handle(self, pid):
        url = assemble_pid_url(self.base_url, pid)
        return requests.get(url, headers=self._get_auth_header(), verify=self.verify)

    def get_handle_by_type(self, pid, type):
        url = assemble_pid_url(self.base_url, pid)
        return requests.get(url, params={'type': type}, headers=self._get_auth_header(), verify=self.verify)

    def put_handle(self, pid_document):
        url = assemble_pid_url(self.base_url, pid_document.get('handle'))

        headers = {
            'Content-Type': 'application/json'
        }
        headers.update(self._get_auth_header())

        return requests.put(url, headers=headers, data=json.dumps(pid_document), verify=self.verify)

    def put_handle_for_urls(self, urls):
        handle = '{}/{}'.format(self.prefix, uuid.uuid1())
        url_entries = []

        index = 1
        for entry_type in urls.keys():
            url = urls[entry_type]
            url_entries.append(create_entry(index, entry_type, url))
            index += 1

        return self.put_handle({
            'handle': handle,
            'values': url_entries
        })

    def delete_handle(self, pid):
        url = assemble_pid_url(self.base_url, pid)
        return requests.delete(url, headers=self._get_auth_header(), verify=self.verify)

    def _get_auth_header(self):
        return {}


class BasicAuthHandleClient(HandleClient):
    '''
        Handle Client implementation that uses `BasicAuth` for authentication
    '''

    def __init__(self, base_url, prefix, https_verify, username, password):
        self.username = username
        self.password = password
        super(BasicAuthHandleClient,self).__init__(base_url, prefix, https_verify)

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
        cred = '{}:{}'.format(self.username,self.password)
        cred_b64_encoded = base64.b64encode(cred.encode('utf-8')).decode('ascii')
        return {'Authorization': 'Basic {}'.format(cred_b64_encoded)}
