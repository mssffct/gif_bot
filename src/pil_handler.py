import configparser
import os

from PIL import Image, ImageDraw, ImageFont

watermark = '@give_me_gif'
config = configparser.ConfigParser()
config.read('config.ini')
temp_path = config['Path']['temp_path']
font_path = config['Path']['font_path']


class PictureWithText:
    def __init__(self, name: str, text: str, font: str):
        self.name = name
        self.text = text
        self.font = font
        self.changed = ''
        self.add_text()

    def add_text(self):
        """
        Adds picture and watermark to users picture
        :return: changed picture
        """
        try:
            original = Image.open(f'{temp_path}/{self.name}.jpg')
            font = ImageFont.truetype(os.path.join(font_path, self.font), 20)
            drawer = ImageDraw.Draw(original)
            drawer.text((50, 50), self.text, (0, 0, 0), font=font)
            drawer.text((10, 10), watermark, (205, 205, 205))
            self.changed = original.save(f'{temp_path}/{self.name}.jpg')
        except FileNotFoundError:
            print('File not found')


class GifPicture:
    def __init__(self, media_group_id, uid: str):
        self.media_group_id = media_group_id
        self.uid = uid
        self.created = []
        self.result = ''
        self.add_watermark()
        self.create_gif()

    def add_watermark(self):
        """
        Prepares gif frames by adding watermark to each frame
        :return: frame with watermark
        """
        for cur_path, directories, files in os.walk(temp_path):
            for image in files:
                file = f'{temp_path}/{image}'
                frame = Image.open(file)
                drawer = ImageDraw.Draw(frame)
                drawer.text((10, 10), watermark, (205, 205, 205))
                frame.save(file)
                self.created.append(frame)

    def create_gif(self):
        """
        Collects frames and creates gif picture
        :return: gif picture
        """
        try:
            self.result = self.created[0].save(
                f'{temp_path}/{self.uid}_{self.media_group_id}.gif',
                save_all=True,
                append_images=self.created[1:],
                optimize=True,
                duration=100,
                loop=0
            )
            return self.result
        except IndexError:
            pass
