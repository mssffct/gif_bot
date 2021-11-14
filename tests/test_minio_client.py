import os

import pytest
from dotenv import load_dotenv
from minio import Minio

from src.minio_client import MinioHandler

load_dotenv()
MINIO_ROOT_USER = os.getenv('MINIO_ROOT_USER')
MINIO_ROOT_PASSWORD = os.getenv('MINIO_ROOT_PASSWORD')
temp_path = os.path.join('temp')


@pytest.fixture()
def minio_client():
    return MinioHandler(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD)


def temp_clean(path):
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        os.remove(file_path)


def test_get_minio_client_function(minio_client):
    # Given MinioHandler object
    minio = minio_client
    # When
    func = minio.get_minio_client(MINIO_ROOT_USER, MINIO_ROOT_PASSWORD)
    # Then
    assert isinstance(func, Minio) is True


def test_get_gifs_function(minio_client):
    # Given MinioHandler object
    # global temp_path
    minio = minio_client
    # When calling function
    os.chdir('temp')
    minio.get_gifs('752272448')
    # Then
    assert len(os.listdir(os.getcwd())) > 0


def test_save_function(minio_client):
    # Given MinioHandler object, file to save
    minio = minio_client
    # When saving file
    test_list = []
    all_gifs = minio.client.list_objects('general', recursive=True)
    for item in all_gifs:
        test_list.append(item.object_name)
    minio.save(obj_name='752272448_13095111081708074', uid='752272448', pic_format='gif')
    # Then
    assert '752272448_13095111081708074.gif' in test_list
    temp_clean(os.getcwd())
