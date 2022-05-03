from io import TextIOWrapper
from pathlib import Path
from typing import List
import re


def parse_attributes(docs_path: Path):

    tf_attributes: List[str] = []
    with open(docs_path) as file:

        arguments = parse_section("Argument Reference", file)
        tf_attributes.extend(arguments)

        attributes = parse_section("Attributes Reference", file)
        tf_attributes.extend(attributes)

    return tf_attributes


def read_section(docs_path: Path, section_name: str):

    items: List[str]
    with open(docs_path) as file:

        items = parse_section(section_name, file)

    return items


def parse_section(name: str, file: TextIOWrapper):

    cur_pos = file.tell()

    section_location = find_section(name, file)

    if not section_location:
        file.seek(cur_pos)
        return []

    items = parse_items(file)

    if not items:
        print(f"Unable to find items in section {name} of {file.name}")

    return items


def parse_items(file: TextIOWrapper):
    attributes: list[str] = []

    while True:

        # We need the  current postion incase we run into the next section
        cur_pos = file.tell()

        line = file.readline()

        if not line:
            print("We have ran out out attributes to parse")
            break

        # If line starts with whitespace its probably a multiline description
        if line.startswith((" ", "\t")):
            continue

        # These should be the attributes we are after
        if line[0] == "*":

            regex = r"`([\w]+)`"

            attribute = re.search(regex, line).group(1)

            attributes.append(attribute)

        # We have reached a new markdown section
        if line[0] == "#":
            file.seek(cur_pos)
            break

    return attributes


def all_sections(docs_path: Path):

    sections: List[str] = []

    with open(docs_path) as file:

        while True:
            line = file.readline()

            # We dont care about the top level sections, only ## and ##
            if line.startswith("##"):
                sections.append(line.strip())

            if not line:
                break

    return sections


def find_section(name: str, file: TextIOWrapper):

    while True:

        cur_pos = file.tell()

        line = file.readline()

        # print(line)

        if line.startswith("#") and name in line:
            return cur_pos + 1

        if not line:
            print(f"Unable to find section {name} in {file.name}")
            raise Exception()
            return None
