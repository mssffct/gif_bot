import os

from minio import Minio

temp_path = os.path.join('..', 'temp')


class MinioHandler:
    def __init__(self, __access, __secret):
        self.__access = __access
        self.__secret = __secret
        self.client = self.get_minio_client(self.__access, self.__secret)

    @staticmethod
    def get_minio_client(__access, __secret):
        return Minio(
            'localhost:9000',
            access_key=__access,
            secret_key=__secret,
            region='ru',
            secure=False
        )

    def put_in_bucket(
            self, bucket_name: str, obj_name: str
    ):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
        self.client.fput_object(
            bucket_name,
            f'{obj_name}',
            file_path=f'{temp_path}\\{obj_name}',
            content_type='application/csv',
        )

    def save(self, obj_name: str, uid: str, pic_format: str):
        if pic_format == 'gif':
            obj_name = f'{obj_name}.{pic_format}'
            self.put_in_bucket(
                bucket_name='general',
                obj_name=obj_name,
            )
        else:
            obj_name = f'{obj_name}.{pic_format}'
            self.put_in_bucket(
                bucket_name=str(uid),
                obj_name=obj_name
            )

    def get_gifs(self, uid: str):
        """
        Yields gifs from general bucket with exact uid
        :param uid:
        :return:
        """
        all_gifs = self.client.list_objects('general', recursive=True)
        for item in all_gifs:
            if item.object_name.startswith(str(uid)):
                response = self.client.get_object(
                    'general', str(item.object_name)
                )
                with open(f'{temp_path}\\{item.object_name}', 'wb') \
                        as file_data:
                    for d in response.stream(32 * 1024):
                        file_data.write(d)
