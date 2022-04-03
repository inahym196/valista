from argparse import ArgumentParser, Namespace
from Profiles import ProfileFactor
from typing import Any
import yaml


def arg_parser() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('src', nargs='?', default='profile.txt', help='input filepath')
    parser.add_argument('dst', nargs='?', help='export filepath')
    parser.add_argument('-n', '--name', default='esxi01', help='profiles yaml\'s root name')
    parser.add_argument('-t', '--type', default='profile', help='source file type')
    return parser.parse_args()


def profile_exporter(args: Namespace) -> None:
    profiles_dict: dict[str, Any] = ProfileFactor(
        filepath=args.src, name=args.name).Profiles.export()
    if args.dst:
        with open(args.dst, mode='w') as f:
            yaml.dump(profiles_dict, f)
    else:
        print(yaml.dump(profiles_dict))


def exec() -> None:
    args = arg_parser()
    if args.type == 'profile':
        profile_exporter(args)


if __name__ == '__main__':
    exec()
