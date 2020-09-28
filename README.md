# easyhandle
A lightweight python package for accessing handle services.

## Installation
This python package can be installed using `pip`.

```
pip install easyhandle 
```

## Getting Started
This library provides different HandleClient classes (e.g. BasicAuthHandleClient), differing in the way authentication is handled.
All clients inherit from the super class `HandleClient`.

### Instantiating the `client` object
To instantiate a client object either use its constructor: 

```
client = HandleClient('https://hdl.handle.net',
                      prefix='TEST',
                      verify=True) 
```

or the respective classmethod `load_from_config`:

```
client = HandleClient.load_from_config({
    'handle_server_url': 'https://hdl.handle.net',
    'prefix': 'TEST',
    'HTTPS_verify': True
})
```

### Usage

**All methods described below return the according `Response` object of the request submitted to the handle server**

To create a new handle entry (_requires authentication_) use the `put_handle` method, e.g.:

```
client.put_handle({
    'handle': 'TEST/0aca26ca-016f-11eb-adc1-0242ac120002'
    'values': [
        {
            'index': 1,
            'type': 'URL',
            'data': {
                'format': 'string',
                'value': 'https://www.google.com'
        }
    ]
})
```

To retrieve a handle record use the `get_handle` method, e.g.:

```
client.get_handle('TEST/0aca26ca-016f-11eb-adc1-0242ac120002')
```

To delete a handle record use the `delete_handle` method, e.g.:
```
client.delete_handle('TEST/0aca26ca-016f-11eb-adc1-0242ac120002')
```

## Available Clients
### BasicAuthHandleClient
Required config properties:

Name|Description|Default
----|-----------|-------
handle_server_url|base url to the handle service|https://hdl.handle.net
prefix|handle prefix used, when new PIDs are issued|
HTTPS_verify|defines wehter the server certificate should be validated| `True`
username|username used for basic authentication|
password|password used for basic authentication|