import sys
from pystock.storage.local_storage import LocalStorage
from pystock.storage.s3_storage import S3Storage
import collections

print("init storage engine")

STORAGE_MAP = {
    'local': LocalStorage,
    's3': S3Storage
}


class StorageEngine:
    @classmethod
    def set(cls, engine):
        cls.engine = engine
        print(f'engine set to {cls.engine}')
        cls.get()

    @classmethod
    def get(cls):
        print(f'engine from {cls.engine}')
        return cls.engine

    @classmethod
    def configure(cls, storage_conf=None):
        if storage_conf is None:
            cls.set(S3Storage('svdh-python'))
            return
        if ('type' not in storage_conf or
                not isinstance(storage_conf['type'], collections.Mapping)):
            raise Exception(
                f"storage_conf['type'] is not a dictionary. storage_conf:{storage_conf}")
        storage_name = next(iter(storage_conf['type'].keys()))
        if storage_name not in STORAGE_MAP:
            raise Exception(f'Unkown storage type {storage_name}')
        storage_class = STORAGE_MAP[storage_name]
        cls.set(storage_class(storage_conf['type'][storage_name]))
