import re
from pattern_rule import var
from parsing import Parsing
from error import Error
from translator import Translator
from sql_connection import sql


def preprocessing_input(_input: str):
    data = _input.lower()
    data = re.sub(r'[^A-Za-z0-9:\s]+(-)', '', data)
    data = data.split(" ")

    if len(data) < 4:
        raise Exception("Jumlah kata minimal 4")

    return data


def main(input_kalimat):
    # db connection
    db = sql()
    # Scanner
    text = input_kalimat
    text = preprocessing_input(text)
    in_token = []
    for t in text:
        if any(_str in t for _str in var.KATA_YANG_TIDAK_DIABAIKAN):
            in_token.append(t)

        for pattern in var.IGNORE_PATTERN:
            if len(re.findall(pattern, t)) > 0:
                in_token.append(t)
                break

    print(f"Scanner -> {in_token}")

    # parsing
    _str = ' '.join(map(str, in_token))
    parsing = Parsing()
    parsing_input = parsing.parsing_input(_str)
    # print(_str)
    if parsing_input:
        # translator
        attribute, attribute_condition, operator, attribute_data, data_length = parsing_input
        print(
            f'attribute: {attribute}\nattribute kondisi: {attribute_condition}\nopertor: {operator}\ndata: {attribute_data}\ndata length: {data_length}')
        translator = Translator(attribute, attribute_condition, operator, attribute_data, data_length)
        # change table to extracted_sigmet if u want using real data
        query = translator.translate_input_into_query(table="extracted_sigmet_test")
        print(f'translator -> {query}')

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

    db.close_connection()


if __name__ == "__main__":
    prompt = "tampilkan seluruh field untuk sigmet yang dirilis pada tanggal 16-05-2011"
    main(prompt)
