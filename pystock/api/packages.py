from pystock.storage.storage_engine import StorageEngine


def search():
    packages = StorageEngine.get().list_packages()
    return list(map(lambda t: {'package_name': t}, packages))
