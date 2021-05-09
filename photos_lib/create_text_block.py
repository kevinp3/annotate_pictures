from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import os

def text_block(date, fname, body=''):

    font_path = os.path.join(os.path.dirname(__file__), 'Fonts/SourceSansPro-Regular.ttf')

    lines = [date, fname] + body.split('\n')
    font = ImageFont.truetype(font_path, 20)
    fy = font.getsize('X')[1] + 6
    height = fy * len(lines) + 10
    widths = [font.getsize(xx)[0] for xx in lines]
    width = max(widths) + 10

    im = Image.new('RGB', (width, height), 'lightgray')
    img_draw = ImageDraw.Draw(im)
    y = 5
    for line in lines:
        img_draw.text((5, y), line, fill='darkslategray', font=font)
        y += fy

    return im

