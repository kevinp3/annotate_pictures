import PIL
from PIL import Image
from PIL.ExifTags import TAGS
import matplotlib.pyplot as plt

import os

from photos_lib import create_text_block

def date_from_metadata(im):
    for tag, value in sorted(im.getexif().items()):
        tname = TAGS.get(tag, 'UnknownTAG')
        # extarcting all the metadata as key and value pairs and converting them from numerical value to string values
        # print(tag, tname, value)
        if tname.lower().startswith('date'):
            return value


def date_from_fpath(fpath):
    names = fpath.split('/')
    for ii, name in enumerate(names[:-1]):
        try:
            year = int(name)
            return ':'.join(names[ii:-1])
        except ValueError:
            pass
    return None




def determine_date(ipath, im):
    """Return date associated with the image.
       May need to attempt different strategies
    """
    # first, lets try
    res1 = date_from_metadata(im)
    res2 = date_from_fpath(ipath)
    return res1 or res2 or 'Unknown Date'


def resize(im, max_size):
    if im.size[0] > max_size[0] or im.size[1] > max_size[1]:
        ratio = min(max_size[0] / im.size[0], max_size[1] / im.size[1])
        new_size = [int(xx * ratio) for xx in im.size]
        newimg = im.resize(new_size)
    else:
        newimg = im.resize(im.size)    # makes freeing memory easier
    return newimg


def combine(photo, text):
    max_height = 1080
    max_width = 1920
    rphoto = resize(photo, (max_width, max_height))
    p_w, p_h = rphoto.size
    t_w, t_h = text.size

    if p_h + t_h <= max_height:
        f_h = p_h + t_h
        f_w = max(p_w, t_w)
        x = 0
        y = p_h
    else:
        f_h = max(p_h, t_h)
        f_w = p_w + t_w
        x = p_w
        y = max(0, p_h - t_h)

    final = Image.new(mode='RGB', size=(f_w, f_h), color='black')
    final.paste(rphoto, (0, 0))
    final.paste(text, (x, y))


    rphoto.close()
    text.close()

    return final


def do_one(ipath, dest, chop):
    level = len(ipath.split('/'))
    indent = '  ' * level
    root, ext = os.path.splitext(dest)
    jpath = root + '.jpg'
    if os.path.exists(jpath):
        print(indent, ipath, "already processed")
        return

    try:
        im = Image.open(ipath)
    except (PIL.UnidentifiedImageError, OSError) as e:
        print('Skipping UnidentifiedImage Format', ipath, e)
        return -1

    final = None
    try:
        # I didn't want to put all this inside the try block, bu PIL
        # loads images lazily, so some OSErrors aren't discovered until later
        date = determine_date(ipath, im)
        shorter_path = ipath
        if chop and ipath.startswith(chop):
            shorter_path = ipath.replace(chop, '')
        text_image = create_text_block.text_block(date, shorter_path)
        print(indent, ipath, im.format, im.size, im.mode, root, ext, jpath, date)
        final = combine(im, text_image)

        final.save(jpath, format='JPEG')
        final.close()

    except (PIL.UnidentifiedImageError, OSError) as e:
        print('Skipping Unloadable JIT image', ipath, e)
        return -2

    finally:
        im.close()
        if final:
            final.close()




