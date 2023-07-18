import re
import json
from pattern_rule import var
from parsing import Parsing
from error import Error
from translator import Translator
from sql_connection import sql
from flask import Flask, request, jsonify

app = Flask(__name__)
table = "extracted_sigmet"

# app-name : kkp-chatbot
# app-name : kkp-chatbot-test

# az webapp up --runtime PYTHON:3.11 --sku B1 --resource-group sigmet_group --name sigmet-chatbot-1 --location southeastasia


def get_polygon_and_raw_sigmet():
    db = sql()
    query = f"SELECT sigmet, polygon FROM {table} WHERE polygon != '' AND release_date = DATE(convert_tz(now(), @@session.time_zone, '+07:00')) AND status = 'Tidak Ada Perubahan Status Sigmet'"
    result = db.search(query)
    db.close_connection()

    return jsonify(result)


def preprocessing_input(_input: str):
    data = _input.lower()
    data = re.sub(r'[^A-Za-z0-9:\s]+(-)', '', data)
    data = data.split(" ")

    if len(data) < 4:
        return jsonify({
            "error": "Jumlah kata minimal 4"
        })

    return data


@app.route('/')
def default_route():  # put application's code here
    return get_polygon_and_raw_sigmet()


@app.get('/chat')
def process_prompt():
    db = sql()
    text = request.args.get('question')
    text = preprocessing_input(text)
    in_token = []
    for t in text:
        if any(_str in t for _str in var.KATA_YANG_TIDAK_DIABAIKAN):
            in_token.append(t)

        for pattern in var.IGNORE_PATTERN:
            if len(re.findall(pattern, t)) > 0:
                in_token.append(t)
                break

    _str = ' '.join(map(str, in_token))
    parsing = Parsing()
    parsing_input = parsing.parsing_input(_str)

    if parsing_input:
        # translator
        attribute, attribute_condition, operator, attribute_data, data_length = parsing_input
        print(
            f'attribute: {attribute}\nattribute kondisi: {attribute_condition}\nopertor: {operator}\ndata: {attribute_data}\ndata length: {data_length}')
        translator = Translator(attribute, attribute_condition, operator, attribute_data, data_length)
        query = translator.translate_input_into_query(table)
        print(f'translator -> {query}')

        fetched_data = db.search(query=query)
        db.close_connection()
        if fetched_data:
            data = json.loads(json.dumps(fetched_data, default=str))
            print(data)
            return jsonify(data)
        else:
            return jsonify({
                "error": "Data sigmet belum diupdate pada hari ini. Mohon cek kemabali dalam 1 jam kemudian"
            })
    else:
        default_error, pattern_matching_error, rule = parsing.get_error_status()
        err = Error(rule)
        if pattern_matching_error is not None:
            err = json.loads(json.dumps(err.rule_error(), default=str))
            # print(json.loads(err.rule_error()))
            return jsonify(err)
        else:
            # print(json.loads(err.default_error()))
            err = json.loads(json.dumps(err.default_error(), default=str))
            # print(json.loads(err.rule_error()))
            return jsonify(err)


if __name__ == '__main__':
    app.run()
