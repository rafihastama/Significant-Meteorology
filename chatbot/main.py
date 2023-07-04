import re

from var import var
from parsing import Parsing
from error import Error


def preprocessing_input(_input: str):
    data = _input.lower()
    data = re.sub(r'[^A-Za-z0-9:\s]+(-)', '', data)
    data = data.split(" ")

    if len(data) < 4:
        raise Exception("Jumlah kata minimal 4")

    return data


def test():
    arr_text = [
        "Tampilkan seluruh field untuk info sigmet terkini",
        "Tampilkan lokasi gunung, posisi gunung dan polygon untuk info sigmet terkini",
        "Tampilkan waktu valid untuk info sigmet terkini",
        "Tampilkan info sigmet terkini dengan ketinggian awan abu vulkanik diatas 2000 meter",
        "Tampilkan info sigmet terkini dengan ketinggian awan abu vulkanik dibawah 5000 kaki",
        "Tampilkan info sigmet terkini untuk flight level 123",
        "Tampilkan info sigmet terkini untuk wilayah penyebaran abu vulkaniknya berada di lintang S0811 E11255",
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
        parsing = Parsing()
        parsing_input = parsing.parsing_input(_str)
        if parsing_input:
            print(True)
        #     # translator
        #     attribute, attribute_condition, operator, attribute_data = parsing_input
        #     print(f'attribute: {attribute}\nattribute condition: {attribute_condition}\nopertor: {operator}\ndata: {attribute_data}\n')
        else:
            print(False)
        #     print("data yang anda input tidak dapat diproses")

        print("=" * 100, end='\n')


def main():
    text = "Tampilkan info sigmet terkini dengan waktu valid dari jam 09:00 hingga 12:12 dan info sigmet terkini dan kode sigmet 12"
    text = preprocessing_input(text)
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
    parsing = Parsing()
    parsing_input = parsing.parsing_input(_str)
    # db = sql_connection.sql()

    if parsing_input:
        # translator
        attribute, attribute_condition, operator, attribute_data = parsing_input
        print(f'attribute: {attribute}\nattribute condition: {attribute_condition}\nopertor: {operator}\ndata: {attribute_data}\n')
        # translator = Translator(attribute, attribute_condition, operator, attribute_data)
        # query = translator.translate_input_into_query()
        # print(f'query -> {query}')

        # fetched_data = db.search(query=query)
        # if len(fetched_data) > 0:
        #     for data in fetched_data:
        #         print(data)
        # else:
        #     print('Data sigmet belum diupdate pada hari ini. Mohon cek kemabali dalam 1 jam kemudian')
    else:
        default_error, pattern_matching_error, rule = parsing.get_error_status()
        err = Error(rule)
        if pattern_matching_error is not None:
            print(err.rule_error())
        else:
            print(err.default_error())

    # db.close_connection()


if __name__ == "__main__":
    main()

    # test()
    # sys.exit()
