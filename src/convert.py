from argparse import Namespace
#import os


class Profiles:
    pass


class ProfileBuilder():
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.raw_lines: list[str] = self.load_textlines(self.filepath)

    def load_textlines(filepath: str):
        pass

    @property
    def profiles() -> list[str]:
        return self.__profiles


def esxi_converter(args: Namespace):
    with open(args.src, encoding='UTF-8') as f:
        textline: str = f.readline()
        if 'installed:' in textline:
            pass


def converter(args: Namespace):
    if args.type == 'esxi':
        profiles: Profiles = ProfileBuilder(filepath=args.src).profiles
        print(profiles)
