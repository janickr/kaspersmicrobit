#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.
import ast
import os
from dataclasses import dataclass
from typing import List

import griffe
from griffe import Extension, Object, ObjectNode, get_logger

logger = get_logger(__name__)


class TranslateDocstrings(Extension):
    def __init__(self, path: str):
        self.translations = {t.docstring: t for t in (read_translation_file(path))}

    def _translate(self, docstring):
        translation = self.translations.get(docstring)
        return translation.translation if translation else docstring

    def on_instance(self, node: ast.AST | ObjectNode, obj: Object) -> None:
        if obj.docstring:
            obj.docstring.value = self._translate(obj.docstring.value)
            # print(f'"{obj.docstring.value}"')


def add_members(m: Object, all_members: List):
    if not m.is_alias:
        all_members.append(m)
        for c in m.members.values():
            add_members(c, all_members)


def get_docstrings(package_name: str):
    parsed = griffe.load(package_name)

    all_members = []
    add_members(parsed, all_members)

    return all_members


def read_translation_file(filename):
    if os.path.isfile(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return read_translations(iter([line for line in f]))
    else:
        return iter(())


def build_translations(all_members, filename):
    existing = read_translation_file(filename)
    translation_map = {t.name: t for t in existing}

    def update_or_create(name, docstring):
        translation = translation_map.get(name)
        if translation:
            translation.docstring = docstring
            return translation
        else:
            return Translation(name, docstring, '')

    translations = [update_or_create(f'{m.kind.name} {m.path}', m.docstring.value) for m in all_members if
                    m.has_docstring]
    return "\n\n".join([t.format() for t in translations])


@dataclass
class Translation:
    name: str
    docstring: str
    translation: str

    def format(self):
        return f'{self.name}\n"""\n{self.docstring}\n"""\n{self.translation}\n"""'


def read_translations(lines):
    name = read_str_part(lines)
    while name:
        yield Translation(name, read_str_part(lines), read_str_part(lines))
        next(lines, None)
        name = read_str_part(lines)


def read_str_part(lines):
    return "".join(read_part(lines)).strip('\n')


def read_part(lines):
    for line in lines:
        if line == '"""\n':
            return
        yield line


def update_messages_in_file(package_name, filename):
    docstrings = build_translations(get_docstrings(package_name), filename)
    with open(filename, 'w', encoding='utf-8') as f:
        print(docstrings, file=f)


if __name__ == '__main__':
    update_messages_in_file('kaspersmicrobit', 'docstrings_nl.txt')
