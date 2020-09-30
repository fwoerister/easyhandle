def assemble_pid_url(base_url, pid):
    if base_url[-1] != '/':
        base_url += '/'

    return '{}api/handles/{}'.format(base_url, pid)


def create_entry(index, type, url):
    return {
        'index': index,
        'type': type,
        'data': {
            'format': 'string',
            'value': url
        }
    }
