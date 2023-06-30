import sys
from decimal import Decimal
from var import var
from translator import Translator
import re


class Parsing:
    def __init__(self):
        self._translator = Translator()

    def format_coordinates(self, coords: str):
        arr = ''.join(map(str, coords)).split(" ")
        _arr = []
        for i in range(len(arr)):
            degree = arr[i][1:len(arr[i]) - 2]
            minute = arr[i][len(arr[i]) - 2:]
            calc = float("{:.2f}".format(float(degree) + (float(minute) / 60.0)))
            _arr.append(calc)

        return f"%{', '.join(map(str, _arr))}%"

    def validate_input(self, Pattern: dict, _string: str, rule: str):
        found = 0
        _field = None
        _res = None
        for field in Pattern:
            match = re.findall(Pattern.get(field), _string)
            if len(match) > 0:
                print(_string)
                _field = field
                selected_field = []
                data_condition = {
                    "str_b": "",  # string befor keyword cond
                    "str_a": "",  # string after keyword cond
                    "con": "",  # value : where
                    "ac": [],  # attribute condition
                    "d": [],  # data
                    "op": []  # operator
                }

                # find condition keyword
                for key_condition in var.condition:
                    for key_data in key_condition:
                        _search = re.search(key_data, _string)
                        if _search:
                            string_location = _search.span()
                            data_condition["con"] = var.condition.get(key_condition)
                            data_condition["str_a"] = _string[string_location[0]:]
                            data_condition['str_b'] = _string[:string_location[0]]

                # find selected field
                for key_attribute in var.attribute:
                    if isinstance(key_attribute, tuple):
                        for key_data in key_attribute:
                            if re.search(key_data, data_condition['str_b']):
                                selected_field.append(var.attribute.get(key_attribute))
                    else:
                        if re.search(key_attribute, data_condition['str_b']):
                            if isinstance(var.attribute.get(key_attribute), dict):
                                for _, value in var.attribute.get(key_attribute).items():
                                    selected_field.append(value)
                            else:
                                selected_field.append(var.attribute.get(key_attribute))

                print(f"selected field -> {selected_field}")

                # find condition field
                for key_attribute in var.attribute_condition:
                    if isinstance(key_attribute, tuple):
                        for key_data in key_attribute:
                            if re.search(key_data, data_condition["str_a"]):
                                data_condition["ac"].append(var.attribute_condition.get(key_attribute))
                    else:
                        if re.search(key_attribute, data_condition["str_a"]):
                            if isinstance(var.attribute_condition.get(key_attribute), dict):
                                for _, value in var.attribute_condition.get(key_attribute).items():
                                    data_condition["ac"].append(var.attribute_condition.get(key_attribute))
                            else:
                                data_condition["ac"].append(var.attribute_condition.get(key_attribute))
                # find data
                for key_data in var.data:
                    if isinstance(var.data.get(key_data), dict):
                        if re.search(var.data.get(key_data).get("pattern"), data_condition['str_a']):
                            if key_data == "current date":
                                value = var.data.get(key_data).get("data")
                            else:
                                value = re.search(var.data.get(key_data).get("data"), data_condition["str_a"]).group()
                            operator = var.data.get(key_data).get("operator")
                            data_condition["d"].append(value)
                            data_condition["op"].append(operator)
                    else:
                        _search = re.search(var.data.get(key_data), data_condition['str_a'])
                        if _search:
                            if key_data == "lintang":
                                data_condition["d"].append(self.format_coordinates(_search.group().__str__()))
                            else:
                                for result in _search.groups():
                                    if result is not None:
                                        data_condition["d"].append(result)
                # find operator
                for key_operator in var.operator:
                    if re.search(key_operator, data_condition["str_a"]):
                        operator = var.operator.get(key_operator)
                        data_condition["op"].append(operator)

                # check if in str b have pattern for current date
                for key, value in var.attribute_condition.items():
                    if value == "release_date" and re.search(key, data_condition["str_b"]):
                        data_condition["ac"].append(value)
                        data_condition["op"].append(var.data.get("current date").get("operator"))
                        data_condition["d"].append(var.data.get("current date").get("data"))

                # print(f"condition -> {data_condition['con']}")
                print(f"attribute condition -> {data_condition['ac']}")
                print(f"operator -> {data_condition['op']}")
                print(f"data -> {data_condition['d']}")

                # sys.exit()

                # if isinstance(match[0], tuple):
                #     _res = list(filter(None, match[0]))
                # else:
                #     _res = list(filter(None, match))
                # # translator
                # query = self._translator.translate_input(rule, _field, _res)
                # print(f'Translator -> {query}')
                # return query

        # if not found and rule == "aturan 1":
        #     _field = []
        #     for key, val in var.DATATABLE_TO_FIELD.items():
        #         if re.search(key, _string):
        #             _field.append(val)
        #     # translator
        #     print(_field)
        #     query = self._translator.translate_input("aturan 1", _field)
        #
        #     if query != 0:
        #         print(f'Tranlator -> {query}')
        #         return query
        #
        #     print('Kalimat yang anda masukan tidak dapat di proses')
        # else:
        #     print("Query yang anda cari tidak ditemukan")

    def parsing_input(self, _string: str):
        if re.match(var.TAMPILKAN, _string):
            print('Parsing -> aturan 1')
            rule = "aturan 1"
            return self.validate_input(var.PATTERN_RULE_TAMPILKAN, _string, rule)

        if re.match(var.BERAPA, _string):
            print('Parsing -> aturan 2')
            rule = "aturan 2"
            return self.validate_input(var.PATTERN_RULE_BERAPA, _string, rule)

        if re.match(var.DIMANA, _string):
            print('Parsing -> aturan 3')
            rule = "aturan 3"
            return self.validate_input(var.PATTERN_RULE_DIMANA, _string, rule)

        if re.match(var.KAPAN, _string):
            print('Parsing -> aturan 4')
            rule = "aturan 4"
            return self.validate_input(var.PATTERN_RULE_KAPAN, _string, rule)

        if re.match(var.APA, _string):
            print('Parsing -> aturan 5')
            rule = "aturan 5"
            return self.validate_input(var.PATTERN_RULE_APA, _string, rule)

        if re.match(var.ARAH, _string):
            print('Parsing -> aturan 6')
            rule = "aturan 6"
            return self.validate_input(var.PATTERN_RULE_ARAH, _string, rule)

        print('Kalimat yang diinputkan tidak dapat di proses')
