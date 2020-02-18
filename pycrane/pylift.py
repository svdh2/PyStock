from pathlib import Path
from bravado.client import SwaggerClient

client = SwaggerClient.from_url('http://0.0.0.0:8080/pystock/swagger.json')


def list_packages():
    return client.packages.get_packages().response().result


def upload_package(path: Path):
    with open(path, "rb") as pkg_data:
        client.bin.post_bin(
            file_to_upload=path.name,
            filecontent=pkg_data.read()
        ).result()


print(f"Before upload - packages:{list_packages()}")

upload_package(Path("./pyline-0.1.tar.gz"))

print(f"After upload - packages:{list_packages()}")


def main():
    pass


if __name__ == "__main__":
    main()
