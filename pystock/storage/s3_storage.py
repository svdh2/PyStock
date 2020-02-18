import os
import sys
import collections
import hashlib

import pprint
import boto3
from botocore.exceptions import ClientError

from pathlib import Path
from typing import List

SUFFIX = ".tar.gz"

PackageInfo = collections.namedtuple("PackageInfo", ['name', 'version'])


class S3Storage:
    """
    Organizes the packages according to the manual repository guidelines https://packaging.python.org/guides/hosting-your-own-index/
    """

    def __init__(self, config):
        self.client = boto3.client('s3')
        self.bucket = config['bucket']
        try:
            self.client.head_bucket(Bucket=self.bucket)
        except:
            raise Exception(f"could not access bucket {bucket}")

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
        package_info = self._file_name_components(package_full_name)
        self.client.put_object(
            Bucket=self.bucket,
            Body=data,
            Key=f'{package_info.name}/{package_full_name}'
        )
        self.client.put_object(
            Bucket=self.bucket,
            Body=hashlib.sha1(data).hexdigest(),
            Key=f'{package_info.name}/{package_full_name}.sha1'
        )

    @staticmethod
    def get_package_full_name(name, version):
        return f'{name}-{version}.tar.gz'

    def get_package_hash(self, name, version):
        package_full_name = S3Storage.get_package_full_name(name, version)
        package_info = self._file_name_components(package_full_name)
        obj = self.client.get_object(
            Bucket=self.bucket,
            Key=f'{package_info.name}/{package_full_name}.sha1'
        )
        return obj['Body'].read().decode('utf-8')

    def get_package_versions(self, name: str) -> List[str]:
        versions = []
        window = self.client.list_objects_v2(Bucket=self.bucket, Delimiter='/', Prefix=f'{name}/')
        if 'Contents' in window:
            versions.extend(map(lambda p: p['Key'],window['Contents']))
            while 'ContinuationToken' in window:
                window = self.client.list_objects_v2(Bucket=self.bucket, Delimiter='/', Prefix=f'{name}/')
                versions.extend(map(lambda p: p['Key'],window['Contents']))
        prefix_len=len(f'{name}/')
        return list(map(lambda p:self._file_name_components(p[prefix_len:]).version,
                        filter(lambda p:p.endswith(SUFFIX),versions)))

    def get_package(self, package_full_name: str) -> bytes:
        package_info = self._file_name_components(package_full_name)
        obj = self.client.get_object(
            Bucket=self.bucket,
            Key=f'{package_info.name}/{package_full_name}'
        )
        return obj['Body'].read()

    def list_packages(self):
        packages = []
        window = self.client.list_objects_v2(Bucket=self.bucket, Delimiter='/')
        if 'CommonPrefixes' in window:
            packages.extend(map(lambda p: p['Prefix'][:-1],window['CommonPrefixes']))
            while 'ContinuationToken' in window:
                window = self.client.list_objects_v2(Bucket=self.bucket, Delimiter='/', Prefix=f'name/')
                packages.extend(map(lambda p: p['Prefix'][:-1],window['CommonPrefixes']))
        return packages
