from argparse import ArgumentParser, Namespace
from converter.Profile import ProfileConverter
from converter.Abstract import BaseConverter


def arg_parser() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('src', nargs='?', default='profile.txt', help='input filepath')
    parser.add_argument('dst', nargs='?', help='output filepath')
    parser.set_defaults(converter=BaseConverter)

    subparsers = parser.add_subparsers()
    subparsers.required = True
    parser_profile = subparsers.add_parser('profile', help='esxi profile converter')
    parser_profile.add_argument('-n', '--name', required=True,
                                help='hostname to which the profile is applied')
    parser_profile.set_defaults(converter=ProfileConverter)

    args = parser.parse_args()
    return args


def converter(args: Namespace) -> None:
    option = vars(args)
    if hasattr(args, 'converter'):
        converter: BaseConverter = args.converter()
        converter.export(input_filepath=args.src, output_filepath=args.dst, option=option)


def exec() -> None:
    args = arg_parser()
    converter(args)


if __name__ == '__main__':
    exec()
