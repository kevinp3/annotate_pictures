import PIL
from PIL import Image
from PIL.ExifTags import TAGS

import os

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
    return (res1, res2)
    if not res:
        # try to retrieve a date from any manual sorting
        res = date_from_fpath(ipath)

    return res


def do_one(ipath, dest):
    try:
        im = Image.open(ipath)
    except PIL.UnidentifiedImageError:
        print('Skipping UnidentifiedImage Format', ipath)
        return -1
    level = len(ipath.split('/'))
    indent = '  ' * level
    root, ext = os.path.splitext(dest)
    jpath = root + '.jpg'
    date = determine_date(ipath, im)
    print(indent, ipath, im.format, im.size, im.mode, root, ext, jpath, date)

    im.save(jpath, format='JPEG')