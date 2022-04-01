from argparse import ArgumentParser
from convert import converter


def arg_parser():
    parser = ArgumentParser()
    parser.add_argument('src', type=str)
    parser.set_defaults(handler=converter)
    return parser.parse_args()


def exec():
    args = arg_parser()
    args.handler(args)


if __name__ == '__main__':
    exec()
