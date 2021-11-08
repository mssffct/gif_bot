import os

from minio import Minio
from minio.error import InvalidResponseError


class MinioHandler:
    def __init__(self, __access, __secret):
        self.__access = __access
        self.__secret = __secret
        self.client = self.get_minio_client(self.__access, self.__secret)

    @staticmethod
    def get_minio_client(__access, __secret):
        return Minio(
            '',
            access_key=__access,
            secret_key=__secret
        )

    def put_object(
            self, bucket_name: str, obj: str, pic_format: str, obj_name: str
    ):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
        try:
            with open(obj, 'rb') as file:
                statdata = os.stat(obj)
                self.client.put_object(
                    bucket_name,
                    obj_name,
                    file,
                    statdata.st_size,
                    content_type=pic_format
                )
        except InvalidResponseError as ident:
            raise

    def save(self, obj, uid: str, pic_format: str):
        if pic_format == 'gif':
            self.put_object(
                bucket_name='general',
                obj=obj,
                pic_format=pic_format,
                obj_name=uid
            )
        else:
            self.put_object(
                bucket_name=uid,
                obj=obj,
                pic_format=pic_format,
                obj_name=obj.name
            )

    def get_gifs(self, uid: str):
        all_gifs = self.client.list_objects('general', recursive=True)
        for item in all_gifs:
            if item.object_name == uid:
                yield self.client.get_object('general', item)
            pass
