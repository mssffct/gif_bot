import pytest
from src.minio_client import MinioHandler
from minio import Minio


@pytest.fixture()
def minio_client():
    return MinioHandler('ACCESS_KEY', 'SECURE_KEY')


def test_get_minio_client_function(minio_client):
    # Given MinioHandler object
    minio = minio_client
    # When
    func = minio.get_minio_client()
    # Then
    assert isinstance(func, Minio) is True


def test_save_function(minio_client):
    # Given MinioHandler object, picture to save
    minio = minio_client
    obj = ''
    # When saving picture
    minio.save(obj, 'uid', 'gif')
    # Then
    assert minio.client.get_object('general', obj) == obj


def test_get_gifs_function(minio_client):
    # Given MinioHandler object
    minio = minio_client
    # When calling function
    gif_pic = minio.get_gifs('uid')
    # Then
    assert gif_pic == minio.client.get_object('general', gif_pic)
