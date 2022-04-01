from argparse import ArgumentParser, Namespace


class VIBs:
    def __init__(self, vibs: list[dict[str, str]]) -> None:
        self.vibs = vibs

    def read(self):
        print('read')

    def export(self):
        print('export')

    def __repr__(self) -> str:
        import pprint
        return "<VIBS '%s'>" % pprint.pprint(self.vibs)


class VIBsFactor:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.raw_text: list[str] = self.load_text(self.filepath)
        self.__vibs: list[dict[str, str]] = self.extract_vibs(self.raw_text)
        self.VIBs = VIBs(self.__vibs)

    @staticmethod
    def load_text(filepath: str) -> list[str]:
        with open(filepath, encoding='UTF-8') as f:
            return f.readlines()

    @staticmethod
    def extract_vibs(text: list[str]) -> list[dict[str, str]]:
        is_VIB_info: bool = False
        vibs: list[dict[str, str]] = list()
        vib: dict[str, str] = dict()
        for line in text:
            if 'The following VIBs are' in line:
                vib = dict()
                is_VIB_info = True
                operation_date = line.split()[0][:-1]
                vib['operation_date'] = operation_date
            elif is_VIB_info == True:
                if '----------' in line:
                    is_VIB_info = False
                    vibs.append(vib)
                elif 'installed:' in line:
                    operation = line.split()[0][:-1]
                    vib['operation'] = operation
                else:
                    name = line.split()[0]
                    version = line.split()[1]
                    vib['name'] = name
                    vib['version'] = version
        return vibs

    @property
    def vibs(self):
        return self.VIBs


def arg_parser() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('src', nargs='?', default='profile.txt', help='input filepath')
    parser.add_argument('-t', '--type', default='esxi', help='source file type')
    parser.add_argument('--save', help='export filepath. default is stdout.')
    return parser.parse_args()


def exec() -> None:
    args = arg_parser()
    if args.type == 'esxi':
        vibsfactor = VIBsFactor(filepath=args.src)
        vibs: VIBs = vibsfactor.vibs
        print(vibs)


if __name__ == '__main__':
    exec()
