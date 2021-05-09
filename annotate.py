import argparse
import sys

from photos_lib import process_folders


def command_line_starter():
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='inroot', help="input root folder")
    parser.add_argument(dest='outroot', help="output root folder")
    parser.add_argument('--chop', default='', help='remove this string prefix from output filenames')
    args = parser.parse_args()

    return process_folders.do_one_tree(args.inroot, args.outroot, chop=args.chop)


if __name__ == '__main__':
    res = command_line_starter()
    sys.exit(res)