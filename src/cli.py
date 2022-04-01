from argparse import ArgumentParser, Namespace
from VIBs import VIBs, VIBsFactor


def arg_parser() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('src', nargs='?', default='profile.txt', help='input filepath')
    parser.add_argument('-t', '--type', default='esxi', help='source file type')
    parser.add_argument('--save', help='export filepath. default is stdout.')
    return parser.parse_args()


def exec() -> None:
    args = arg_parser()
    if args.type == 'esxi':
        vibs: VIBs = VIBsFactor(filepath=args.src).VIBs
        print(vibs)


if __name__ == '__main__':
    exec()
