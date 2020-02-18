import connexion
from connexion.resolver import RestyResolver
import dominate
from dominate.tags import *

from flask import Response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from pystock.storage.storage_engine import StorageEngine
from pystock.config import config_parser

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = connexion.FlaskApp(__name__, specification_dir='openapi/', resolver=RestyResolver('pystock.api'))
app.add_api('stock.yaml')

config = config_parser.load_config()
StorageEngine.configure(config.get(config_parser.storage_section))

auth = HTTPBasicAuth()

users = {
    "svdh": generate_password_hash("test")
}

print(f'config: {config_parser.load_config()}')

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

@app.route('/')
@auth.login_required
def packages_index():
    logger.info(f'user "{auth.username()}" accessed the general package index')
    doc = dominate.document(title='Packages Index')

    with doc.head:
        title('Simple Index')
        meta(name='api-version',value="2")

    with doc:
        for p in StorageEngine.get().list_packages():
            a(p,href=f"/{p}")
    return str(doc)


@app.route('/<pkg_name>')
@auth.login_required
def package_info(pkg_name):
    logger.info(f'user "{auth.username()}" accessed the versions index of package index "{pkg_name}"')
    doc = dominate.document(title='Package Info')

    with doc.head:
        title(f'Links for {pkg_name}')
        meta(name='api-version',value="2")

    with doc:
        h1(f'Links for {pkg_name}')
        for v in StorageEngine.get().get_package_versions(pkg_name):
            a(f'{pkg_name}-{v}.tar.gz',rel="internal",href=f'/bin/{pkg_name}-{v}.tar.gz#sha1={StorageEngine.get().get_package_hash(pkg_name,v)}')
    return str(doc)


@app.route('/bin/<pkg_name>')
@auth.login_required
def package_download(pkg_name):
    logger.info(f'user "{auth.username()}" downloaded the package "{pkg_name}"')
    returnfile = StorageEngine.get().get_package(pkg_name)
    return Response(returnfile,
                    mimetype="text/csv",
                    headers={"Content-disposition":
                                 f"attachment; filename={pkg_name}"})



app.run(port=8080)
