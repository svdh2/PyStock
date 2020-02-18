import os
import sys
import collections
import hashlib

from pathlib import Path
from typing import List

SUFFIX = ".tar.gz"

PackageInfo = collections.namedtuple("PackageInfo", ['name', 'version'])


class LocalStorage:
    """
    Organizes the packages according to the manual repository guidelines https://packaging.python.org/guides/hosting-your-own-index/
    """

    def __init__(self, config):
        root = config.get('root','\tmp\python_packages')
        if isinstance(root, str):
            self.root = Path(root)
        else:
            assert root is Path
            self.root = root
        assert self.root.is_dir()

    def _file_name_components(self, filename: str):
        print(f'filename:{filename}')
        assert '-' in filename
        assert (filename.endswith(SUFFIX))
        args = filename.split('-')
        print(f'args:{args}')
        return PackageInfo(args[0],
                           args[1][:-len(SUFFIX)])

    def new_package(self, package_full_name: str, data: bytes):
        """

        :param name: For example pyline-0.1.tar.gz
        :param data: binary content of the package
        :return:
        """
        ##needs to be hardened. The path parameter can be abused
        package_info = self._file_name_components(package_full_name)
        package_dir = Path(self.root, package_info.name)
        package_dir.mkdir(exist_ok=True)
        dest_file_path = Path(package_dir, package_full_name)
        dest_file_path.write_bytes(data)
        dest_file_path_hash = Path(dest_file_path.parent, dest_file_path.name + ".sha1")
        dest_file_path_hash.write_text(hashlib.sha1(data).hexdigest())

    @staticmethod
    def get_package_full_name(name, version):
        return f'{name}-{version}.tar.gz'

    def get_package_hash(self, name, version):
        package_full_name = LocalStorage.get_package_full_name(name, version)
        package_info = self._file_name_components(package_full_name)
        package_dir = Path(self.root, package_info.name)
        hash_file_path = Path(package_dir, package_full_name + ".sha1")
        return hash_file_path.read_text()

    def set_package_description(self, name, description):
        package_dir = Path(self.root, name)
        if not (package_dir.exists() and package_dir.is_dir()):
            raise Exception("package does not exist")
        description_path = Path(package_dir, "description.txt")
        description_path.write_text(description)

    def get_package_description(self, name) -> str:
        package_dir = Path(self.root, name)
        if not (package_dir.exists() and package_dir.is_dir()):
            raise Exception("package does not exist")
        description_path = Path(package_dir, "description.txt")
        return description_path.read_text()

    def get_package_versions(self, name: str) -> List[str]:
        package_dir = Path(self.root, name)
        return list(map(lambda f: self._file_name_components(f.name).version,
                        package_dir.glob(f"*{SUFFIX}")))

    def get_package(self, package_full_name: str) -> bytes:
        package_info = self._file_name_components(package_full_name)
        package_dir = Path(self.root, package_info.name)
        dest_file_path = Path(package_dir, package_full_name)
        return dest_file_path.read_bytes()

    def list_packages(self):
        return list(map(lambda p: p.name, self.root.glob("*")))
