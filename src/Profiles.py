from dataclasses import dataclass, field
from typing import Union
import re


@dataclass
class Vib:
    name: str
    version: str


Vibs = list[Vib]


@dataclass
class Profile:
    apply_date: str = ''
    operation: str = ''
    vibs: Vibs = field(default_factory=list)


@dataclass
class Profiles:
    profiles: list[Profile] = field(default_factory=list)

    def export(self) -> list[Profile]:
        return self.profiles


class ProfileFactor:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.raw_text: list[str] = self.load_text(self.filepath)
        self.__profiles: list[Profile] = self.conv_profiles(self.raw_text)
        self.__Profiles = Profiles(self.__profiles)

    @staticmethod
    def load_text(filepath: str) -> list[str]:
        with open(filepath, encoding='UTF-8') as f:
            return f.readlines()

    @staticmethod
    def parse_profile_element(line: str) -> Union[dict[str, str], Vib]:
        profile_element: dict[str, str] = dict()
        operations = [
            {
                'matchword': 'installed',
                'keyword': 'install'
            },
            {
                'matchword': 'removed',
                'keyword': 'remove'
            }
        ]
        apply_date_pattern = re.compile(r'The folowing VIBs are')

        if re.match(apply_date_pattern, line):
            profile_element['apply_date'] = line.split()[0][:-1]
            return profile_element

        for ope in operations:
            if ope['matchword'] in line:
                profile_element['operation'] = ope['keyword']
                return profile_element
        else:
            vib = Vib(name=line.split()[0], version=line.split()[1])
            return vib

    def parse_profile(self, line: str) -> Profile:
        profile = Profile()
        profile_element = self.parse_profile_element(line)

        if isinstance(profile_element, Vib):
            profile.vibs = [profile_element]
        else:
            profile = Profile(**profile_element)

        return profile

    def conv_profiles(self, text: list[str]) -> list[Profile]:

        is_parsable_line: bool = False
        start_word = 'The following VIBs are'
        end_word = '----------'
        profiles: list[Profile] = list()
        profile = Profile()

        for line in text:
            if start_word in line:
                is_parsable_line = True
            elif end_word in line:
                is_parsable_line = False
                profiles.append(profile)

            if is_parsable_line:
                profile = self.parse_profile(line)

        return profiles

    @ property
    def Profiles(self) -> Profiles:
        return self.__Profiles
