from argparse import ArgumentParser, Namespace
from Profiles import ProfileConverter


def arg_parser() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('src', nargs='?', default='profile.txt', help='input filepath')
    parser.add_argument('dst', nargs='?', help='export filepath')
    parser.add_argument('-n', '--name', default='esxi01', help='profiles yaml\'s root name')
    parser.add_argument('-t', '--type', default='profile', help='source file type')
    return parser.parse_args()


def converter(args: Namespace) -> None:
    src_filepath = args.src
    dst_filepath = args.dst
    name = args.name
    type = args.type
    if type == 'profile':
        ProfileConverter(src_filepath, name).export(dst_filepath)


def exec() -> None:
    args = arg_parser()
    converter(args)


if __name__ == '__main__':
    exec()
