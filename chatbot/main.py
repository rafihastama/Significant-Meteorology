import re
import sys

from var import var
from parsing import Parsing


def preprocessing_input(_input: str):
    data = _input.lower()
    data = re.sub(r'[^A-Za-z0-9:\s]+(-)', '', data)
    data = data.split(" ")

    if len(data) < 4:
        raise Exception("Jumlah kata minimal 4")

    return data


def main():
    # scanner
    text = "Kearah mana abu vulkanik untuk sigmet 15 bergerak"
    text = preprocessing_input(text)

    # token
    in_token = []
    for t in text:
        if any(_str in t for _str in var.KATA_YANG_TIDAK_DIABAIKAN):
            in_token.append(t)

        for pattern in var.IGNORE_PATTERN:
            if len(re.findall(pattern, t)) > 0:
                in_token.append(t)
                break

    print(f"Token - > {in_token}")

    # parsing
    _str = ' '.join(map(str, in_token))
    print(_str)
    _parsing = Parsing()

    _parsing.parsing_input(_str)


if __name__ == "__main__":
    main()
