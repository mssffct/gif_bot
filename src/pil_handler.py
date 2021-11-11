from PIL import Image, ImageDraw, ImageFont
import io
import os


watermark = '@give_me_gif'


class PictureWithText:
    def __init__(self, picture, text: str, font: str):
        self.picture = picture
        self.text = text
        self.font = font
        self.changed = ''
        self.add_text()

    def add_text(self):
        try:
            original = Image.open(io.BytesIO(self.picture))
            font = ImageFont.truetype(os.path.join('fonts', self.font), 20)
            drawer = ImageDraw.Draw(original)
            drawer.text((50, 50), self.text, (0, 0, 0), font=font)
            drawer.text((10, 10), watermark, (205, 205, 205))
            self.changed = original
        except FileNotFoundError:
            print('File not found')


class GifPicture:
    def __init__(self, frames: list):
        self.frames = frames
        self.created = []
        self.create_gif()

    def create_gif(self):
        pass
        # for item in self.frames:
        #     frame = Image.open(io.BytesIO(item))
        #     drawer = ImageDraw.Draw(frame)
        #     drawer.text((10, 10), watermark, (205, 205, 205))
        #     self.created.append(item)
        # for item in self.created:
        #     item.show()
