def assemble_pid_url(base_url, pid):
    if base_url[-1] != '/':
        base_url += '/'

    return f'{base_url}api/handles/{pid}'


def create_entry(index, type, url):
    return {
        'index': index,
        'type': type,
        'data': {
            'format': 'string',
            'value': url
        }
    }
