from pystock.storage.storage_engine import StorageEngine
import connexion

def get():
    return list(map(lambda name:{'package_name': name}, StorageEngine.get().list_packages()))

def post(file_to_upload):
    print(f'filename:{file_to_upload}')
    StorageEngine.get().new_package(file_to_upload,connexion.request.files['filecontent'].read())
    return
