import json
import logging
import os
import shutil
import xml.dom.minidom
from xml.dom.minidom import Document

logger = logging.getLogger('fs_util')


def make_dir(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise Exception(f"Path exists but not a directory: '{path}'")
    else:
        os.makedirs(path)
        logger.info("Make directory: '%s'", path)


def delete_file(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
    if os.path.exists(path):
        if not os.path.isfile(path):
            raise Exception(f"Path not a file: '{path}'")
        os.remove(path)
        logger.info("Delete file: '%s'", path)


def delete_dir(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise Exception(f"Path not a directory: '{path}'")
        shutil.rmtree(path)
        logger.info("Delete directory: '%s'", path)


def delete_item(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
    if os.path.isfile(path):
        os.remove(path)
        logger.info("Delete file: '%s'", path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
        logger.info("Delete directory: '%s'", path)


def copy_the_file(
        name: str | bytes | os.PathLike[str] | os.PathLike[bytes],
        dir_from: str | bytes | os.PathLike[str] | os.PathLike[bytes],
        dir_to: str | bytes | os.PathLike[str] | os.PathLike[bytes],
):
    path_from = os.path.join(dir_from, name)
    path_to = os.path.join(dir_to, name)
    shutil.copyfile(path_from, path_to)
    logger.info("Copy file: '%s' -> '%s'", path_from, path_to)


def copy_the_dir(
        name: str | bytes | os.PathLike[str] | os.PathLike[bytes],
        dir_from: str | bytes | os.PathLike[str] | os.PathLike[bytes],
        dir_to: str | bytes | os.PathLike[str] | os.PathLike[bytes],
):
    path_from = os.path.join(dir_from, name)
    path_to = os.path.join(dir_to, name)
    shutil.copytree(path_from, path_to)
    logger.info("Copy directory: '%s' -> '%s'", path_from, path_to)


def copy_the_item(
        name: str | bytes | os.PathLike[str] | os.PathLike[bytes],
        dir_from: str | bytes | os.PathLike[str] | os.PathLike[bytes],
        dir_to: str | bytes | os.PathLike[str] | os.PathLike[bytes],
):
    path_from = os.path.join(dir_from, name)
    path_to = os.path.join(dir_to, name)
    if os.path.isfile(path_from):
        shutil.copyfile(path_from, path_to)
        logger.info("Copy file: '%s' -> '%s'", path_from, path_to)
    elif os.path.isdir(path_from):
        shutil.copytree(path_from, path_to)
        logger.info("Copy directory: '%s' -> '%s'", path_from, path_to)


def read_str(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> str:
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()


def write_str(text: str, path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(text)


def read_json(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> dict | list:
    return json.loads(read_str(path))


def write_json(data: dict | list, path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
    text = json.dumps(data, indent=2, ensure_ascii=False)
    write_str(f'{text}\n', path)


def read_xml(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> Document:
    return xml.dom.minidom.parse(path)


def write_xml(dom: Document, path: str | bytes | os.PathLike[str] | os.PathLike[bytes]):
    xml_str = dom.toprettyxml(indent=' ' * 4, newl='\n', encoding='utf-8')
    with open(path, 'wb') as file:
        for line in xml_str.splitlines():
            if line.strip() == b'':
                continue
            file.write(line.replace(b'?>', b' ?>').replace(b'/>', b' />'))
            file.write(b'\n')
