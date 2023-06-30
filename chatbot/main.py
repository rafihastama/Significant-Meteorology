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
    arr_text = [
        "Tampilkan seluruh field untuk info sigmet terkini",
        "Tampilkan lokasi gunung, posisi gunung dan polygon untuk kode sigmet 12",
        "Tampilkan waktu valid untuk info sigmet terkini",
        "Tampilkan info sigmet terkini dengan ketinggian awan abu vulkanik diatas 2000 meter",
        "Tampilkan info sigmet terkini dengan ketinggian awan abu vulkanik dibawah 5000 kaki",
        "Tampilkan info sigmet terkini untuk flight level 123",
        "Tampilkan info sigmet terkini untuk wilayah penyebaran abu vulkaniknya berada di lintang s1235 e12356",
        "Tampilkan info sigmet terkini dengan waktu valid dari jam 09:00 hingga 12:11",
        "Tampilkan wilayah penyebaran abu vulkanik untuk kode sigmet 12",
        "Berapa lama waktu valid untuk kode sigmet 99",
        "Berapa ketinggian abu vulkanik untuk kode sigmet 21",
        "Berapa kecepatan abu vulkanik untuk kode sigmet 21",
        "Dimana lokasi gunung untuk kode sigmet 99",
        "Dimana lokasi dikeluarkannya untuk info sigmet terkini",
        "Dimana titik penyebaran abu vulkanik untuk info sigmet terkini",
        "Kapan waktu dikeluarkannya untuk kode sigmet 14",
        "Kapan waktu diobservasinya untuk info sigmet terkini",
        "Apa status untuk info sigmet terkini",
        "Apa intensitas abu vulkanik untuk kode sigmet 99",
        "Kearah mana pergerakan abu vulkanik untuk info sigmet terkini"
    ]

    for val in arr_text:
        text = preprocessing_input(val)
        print(f'Scanner -> {text}')

        # token
        in_token = []
        for t in text:
            if any(_str in t for _str in var.KATA_YANG_TIDAK_DIABAIKAN):
                in_token.append(t)

            for pattern in var.IGNORE_PATTERN:
                if len(re.findall(pattern, t)) > 0:
                    in_token.append(t)
                    break

        print(f"Token -> {in_token}")

        # parsing
        _str = ' '.join(map(str, in_token))
        _parsing = Parsing()
        _parsing.parsing_input(_str)
        print("="*100, end="\n")



if __name__ == "__main__":
    main()
    # text = "Tampilkan info sigmet terkini untuk wilayah penyebaran abu vulkaniknya berada di lintang s1235 e12356"
    # text = preprocessing_input(text)
    # print(f'Scanner -> {text}')
    #
    # # token
    # in_token = []
    # for t in text:
    #     if any(_str in t for _str in var.KATA_YANG_TIDAK_DIABAIKAN):
    #         in_token.append(t)
    #
    #     for pattern in var.IGNORE_PATTERN:
    #         if len(re.findall(pattern, t)) > 0:
    #             in_token.append(t)
    #             break
    #
    # print(f"Token -> {in_token}")
    #
    # # parsing
    # _str = ' '.join(map(str, in_token))
    # _parsing = Parsing()
    # _parsing.parsing_input(_str)
