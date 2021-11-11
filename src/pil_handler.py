from PIL import Image, ImageDraw
import io


class PictureWithText:
    def __init__(self, picture, text: str):
        self.picture = picture
        self.text = text
        self.add_text()

    def add_text(self):
        try:
            original = Image.open(io.BytesIO(self.picture))
            draw = ImageDraw.Draw(original)
            draw.text((0, 0), self.text, (255, 255, 255))
            return original
        except FileNotFoundError:
            print('File not found')
