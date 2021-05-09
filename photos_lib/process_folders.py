import os

from . import process_photo

def do_one_folder(dirpath, fnames, dest, chop):
    os.makedirs(dest, exist_ok=True)
    for fname in fnames:
        iname = os.path.join(dirpath, fname)
        oname = os.path.join(dest, fname)
        process_photo.do_one(iname, oname, chop)

def do_one_tree(inroot, outroot, subfolder='', chop=''):
    this_folder = os.path.join(inroot, subfolder)
    was = None
    for dirpath, dnames, fnames in os.walk(this_folder):
        if not was:
            was = dirpath
        tobe = dirpath.replace(was, '')
        dest = os.path.join(outroot, tobe)
        do_one_folder(dirpath, fnames, dest, chop)

