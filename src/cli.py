from argparse import ArgumentParser, Namespace
from Profiles import Profiles, ProfileFactor
import yaml


def arg_parser() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('src', nargs='?', default='profile.txt', help='input filepath')
    parser.add_argument('dst', nargs='?', help='export filepath')
    parser.add_argument('-t', '--type', default='profile', help='source file type')
    return parser.parse_args()


def profile_exporter(args: Namespace) -> None:
    profiles: Profiles = ProfileFactor(filepath=args.src).Profiles
    if args.dst:
        with open(args.dst, mode='w') as f:
            yaml.dump(profiles.profiles, f)
    else:
        print(yaml.dump(profiles.profiles))


def exec() -> None:
    args = arg_parser()
    if args.type == 'profile':
        profile_exporter(args)


if __name__ == '__main__':
    exec()
