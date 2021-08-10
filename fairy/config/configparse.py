'''
Author : hupeng
Time : 2021/8/9 11:10 
Description: 
'''
import os
import re
from typing import (
    Any,
    List,
    Dict,
    AnyStr,
)

from cached_property import cached_property

__all__ = ['ConfigParser']


class Str(str):
    BOOLEAN_STATES = {'1': True, 'yes': True, 'true': True, 'on': True,
                      '0': False, 'no': False, 'false': False, 'off': False}
    STRIP = ''' '"'''
    __int = int
    __dict = dict

    @cached_property
    def _bool(self) -> bool:
        _str = self.__str__()
        if _str.lower() not in self.BOOLEAN_STATES:
            raise ValueError('Not a boolean: %s' % _str)
        return self.BOOLEAN_STATES[_str.lower()]

    @cached_property
    def _int(self) -> int:
        return self.__int(self.__str__())

    @cached_property
    def _list(self) -> List[AnyStr]:
        _str = self.__str__()
        if not (_str.startswith('[') and _str.endswith(']')):
            raise ValueError("can't convert list object")
        return [_.strip(self.STRIP) for _ in _str.strip('[]').split(',')]

    @cached_property
    def _dict(self) -> Dict[str, str]:
        _str = self.__str__()
        if not (_str.startswith('{') and _str.endswith('}')):
            raise ValueError("can't convert dict object")
        _l = [_.strip(self.STRIP).split(':', 1) for _ in _str.strip('{}').split(',')]
        return self.__dict(_l)


class Section(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        s = f'{self.name} section info:\n'
        for key, value in self.__dict__.items():
            s += f'{key}: {value}\n'
        return s


class BaseConfigParser(object):
    _SECTION_PATTERN = '\[(?P<header>[^]]+)\]'
    _OPT_TMPL = '(?P<option>.*?)\s*(?P<vi>{delim})\s*(?P<value>.*)$'

    SECTCRE = re.compile(_SECTION_PATTERN, re.VERBOSE)
    OPTCRE = re.compile(_OPT_TMPL.format(delim="=|:"), re.VERBOSE)
    _KEYCRE = re.compile(r"%\((?P<key>[^)]+)\)s")

    def before_set(self, section: Section, value: Any) -> Any:
        tmp_value = value.replace('%%', '')  # escaped percent signs
        tmp_value = self._KEYCRE.sub('', tmp_value)  # valid syntax
        if '%' in tmp_value:
            raise ValueError("invalid interpolation syntax in %r at "
                             "position %d" % (value, tmp_value.find('%')))
        replace_k = self._KEYCRE.search(value)
        if replace_k is not None:
            replace_option = replace_k.group('key')
            if not hasattr(section, replace_option):
                raise ValueError(f'section {section.name} not have option {replace_option}')
            value = getattr(section, replace_option) + tmp_value
        return value


class ConfigParser(BaseConfigParser):
    def __init__(self):
        self._sections = {}

    def __getattr__(self, item):
        # print(item)
        return self.section(item)

    @property
    def sections(self):
        return list(self._sections.keys())

    def section(self, name):
        if name in self._sections:
            return self._sections[name]
        raise AttributeError(f"No section: '{name}'")

    def read(self, filenames: str, encoding: str = 'utf-8-sig') -> List[str]:
        if isinstance(filenames, (str, os.PathLike)):
            filenames = [filenames]

        read_ok = []
        for filename in filenames:
            try:
                with open(filename, encoding=encoding) as fp:
                    self._read(fp, filename)
            except OSError:
                continue
            if isinstance(filename, os.PathLike):
                filename = os.fspath(filename)
            read_ok.append(filename)
        return read_ok

    def _read(self, fp: open, fpname: str) -> None:
        lines = [line for line in fp.readlines() if line.strip() and (not line.strip().startswith(';'))
                 and (not line.strip().startswith('#'))]
        if not lines:
            raise (f'{fpname} can not be empty!')
        section = Section(self.SECTCRE.match(lines[0]).group('header'))
        sections = [section]
        self.sections.append(section.name)
        # print(section.name)
        for line in lines[1:]:
            sec_str = self.SECTCRE.match(line)
            if sec_str:
                sec_name = sec_str.group('header')
                section = Section(sec_name)
                sections.append(section)
                # self.sections.append(section.name)

            opt = self.OPTCRE.search(line)
            if opt:
                option, _, value = opt.groups()
                value = self.before_set(section, value)
                # print(option, value)
                setattr(section, option, Str(value))

        for sec in sections:
            self._sections[sec.name] = sec
            # setattr(self, sec.name, sec)


if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini')
    # print(config.sections)
    print(config.log.log_dir)
    print(config.db.port._int, type(config.db.port._int))
    print(config.server.debug._bool, type(config.server.debug._bool))
    print(config.oxk.high._list, type(config.oxk.high._list))
    print(config.oxk.high._list, type(config.oxk.high._list))
    print(config.oxk.high._list, type(config.oxk.high._list))
    # print(config.l.di._dict())
