from typing import Union, Any
import yaml
import re
from dataclasses import asdict

from Profiles import Profile, Profiles, Vib


class ProfileConverter:
    def __init__(self, filepath: str, name: str) -> None:
        self.filepath = filepath
        self.name = name
        self.raw_text: list[str] = self.load_text(self.filepath)
        self.profiles = self.conv_profiles(self.raw_text, name)
        self.Profiles = Profiles(self.profiles)

    @ staticmethod
    def load_text(filepath: str) -> list[str]:
        with open(filepath, encoding='UTF-8') as f:
            return f.readlines()

    @ staticmethod
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
            profile_element['apply_date'] = line.split()[0][: -1]
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

    def conv_profiles(self, text: list[str], name: str) -> dict[str, list[Profile]]:

        is_parsable_line: bool = False
        start_word = 'The following VIBs are'
        end_word = '----------'
        profile = Profile()
        profiles_name = name
        profiles_value: list[Profile] = list()

        for line in text:
            if start_word in line:
                is_parsable_line = True
            elif end_word in line:
                is_parsable_line = False
                profiles_value.append(profile)

            if is_parsable_line:
                profile = self.parse_profile(line)

        profiles: dict[str, list[Profile]] = dict()
        profiles[profiles_name] = profiles_value
        return profiles

    def export(self, filepath: str = ''):
        profiles_dict: dict[str, Any] = asdict(self.Profiles)
        if filepath == '':
            with open(filepath, mode='w') as f:
                yaml.dump(profiles_dict, f)
        else:
            print(yaml.dump(profiles_dict))
