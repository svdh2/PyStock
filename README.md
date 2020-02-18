

# How to run the server
## Staight in the shell
```
PYTHONPATH=. pipenv run gunicorn pystock.server:app
```

## Via docker



# how to install from the repo

If the server runs on your local machine

```
pipenv sync
pipenv install --extra-index-url 127.0.0.1:8080 <package>
```

If you have an url for the server

```
pipenv install --extra-index-url 127.0.0.1:8080 <package>
```


#how to upload a package from a script
```
clear; pipenv run python pycrane/pylift.py
```

#how to build a client
```python
from pathlib import Path
from bravado.client import SwaggerClient

client = SwaggerClient.from_url('http://0.0.0.0:8080/pystock/swagger.json')

def list_packages():
    return client.packages.get_packages().response().result

def upload_package(path:Path):
    with open(path, "rb") as pkg_data:
        client.bin.post_bin(
            file_to_upload=path.name,
            filecontent= pkg_data.read()
        ).result()
```

# For developers

pipenv run connexion run pystock/openapi/stock.yaml --mock=all -v

http://0.0.0.0:5000/pystock/ui/#/default

http://0.0.0.0:5000/pystock/swagger.json

