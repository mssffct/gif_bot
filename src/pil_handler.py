import os

from PIL import Image, ImageDraw, ImageFont

watermark = '@give_me_gif'


class PictureWithText:
    def __init__(self, name: str, text: str, font: str):
        self.name = name
        self.text = text
        self.font = font
        self.changed = ''
        self.add_text()

    def add_text(self):
        try:
            original = Image.open(f'../temp/{self.name}.jpg')
            font = ImageFont.truetype(os.path.join('fonts', self.font), 20)
            drawer = ImageDraw.Draw(original)
            drawer.text((50, 50), self.text, (0, 0, 0), font=font)
            drawer.text((10, 10), watermark, (205, 205, 205))
            self.changed = original.save(f'../temp/{self.name}.jpg')
        except FileNotFoundError:
            print('File not found')


class GifPicture:
    def __init__(self, media_group_id, uid: str):
        self.path = '../temp/'
        self.media_group_id = media_group_id
        self.uid = uid
        self.created = []
        self.result = ''
        self.add_watermark()
        self.create_gif()

    def add_watermark(self):
        for cur_path, directories, files in os.walk(self.path):
            for image in files:
                file = f'{self.path}{image}'
                frame = Image.open(file)
                drawer = ImageDraw.Draw(frame)
                drawer.text((10, 10), watermark, (205, 205, 205))
                frame.save(file)
                self.created.append(frame)

    def create_gif(self):
        try:
            self.result = self.created[0].save(
                f'../temp/{self.uid}_{self.media_group_id}.gif',
                save_all=True,
                append_images=self.created[1:],
                optimize=True,
                duration=100,
                loop=0
            )
            return self.result
        except IndexError:
            pass
