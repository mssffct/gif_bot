import configparser

from minio import Minio

config = configparser.ConfigParser()
config.read('config.ini')
temp_path = config['Path']['temp_path']


class MinioHandler:
    def __init__(self, host_port: str, access: str, secret: str):
        self.host_port = host_port
        self.access = access
        self.secret = secret
        self.client = self.get_minio_client(
            self.host_port, self.access, self.secret
        )

    @staticmethod
    def get_minio_client(host_port: str, access: str, secret: str):
        return Minio(
            endpoint=host_port,
            access_key=access,
            secret_key=secret,
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
            file_path=f'{temp_path}/{obj_name}',
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
                    'general', item.object_name
                )
                with open(f'{temp_path}/{item.object_name}', 'wb') \
                        as file_data:
                    for d in response.stream(32 * 1024):
                        file_data.write(d)
