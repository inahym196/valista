import re
import yaml
from typing import Any
from dataclasses import dataclass, field, asdict
from converter.Abstract import BaseConverter
from utils import load_text


@dataclass
class Vib:
    name: str
    version: str


@dataclass
class Profile:
    apply_date: str = ''
    operation: str = ''
    vibs: list[Vib] = field(default_factory=list)


@dataclass
class Profiles:
    hosts: list[str] = field(default_factory=list)
    profiles: list[Profile] = field(default_factory=list)


class ProfileConverter(BaseConverter):

    def matches_apply_date_pattern(self, line: str) -> bool:
        apply_date_pattern = re.compile(r'The following VIBs are')
        if re.search(apply_date_pattern, line):
            return True
        return False

    def matches_operation_pattern(self, line: str) -> str:
        operations = ['installed', 'removed']
        for ope in operations:
            if ope in line:
                return ope
        return ''

    def parse_vib(self, line: str) -> Vib:
        vib = Vib(name=line.split()[0], version=line.split()[1])
        return vib

    def parse_profile(self, lines: list[str]) -> Profile:
        profile = Profile()
        for line in lines:
            operation = self.matches_operation_pattern(line)
            if self.matches_apply_date_pattern(line):
                profile.apply_date = line.split()[0][: -1]
            elif operation != '':
                profile.operation = operation
            else:
                vib = self.parse_vib(line)
                profile.vibs.append(vib)

        return profile

    def conv_profiles(self, text: list[str], name: str) -> Profiles:

        profiles = Profiles(hosts=[name])
        start_word = 'The following VIBs are'
        end_word = '----------'
        is_parsable_line: bool = False
        parsable_lines: list[str] = list()

        for line in text:
            if start_word in line:
                is_parsable_line = True
            elif end_word in line:
                is_parsable_line = False
                profile = self.parse_profile(parsable_lines)
                profiles.profiles.append(profile)

            if is_parsable_line:
                parsable_lines.append(line)
                continue

        return profiles

    def export(self, input_filepath: str = '', output_filepath: str = '', option: dict[str, Any] = dict()):
        name = option['name']
        raw_text: list[str] = load_text(input_filepath)
        profiles = self.conv_profiles(raw_text, name)
        profiles_dict = asdict(profiles)
        if output_filepath:
            with open(output_filepath, mode='w') as f:
                yaml.dump(profiles_dict, f)
        else:
            print(yaml.dump(profiles_dict))
