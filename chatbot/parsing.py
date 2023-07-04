from var import var
from datetime import datetime
import re


class Parsing:
    def __init__(self):
        self.rule_error = None
        self.rule = None
        self.default_error = None

    def __format_coordinates__(self, coords: str):
        arr = ''.join(map(str, coords)).split(" ")
        _arr = []
        for i in range(len(arr)):
            degree = arr[i][1:len(arr[i]) - 2]
            minute = arr[i][len(arr[i]) - 2:]
            calc = float("{:.2f}".format(float(degree) + (float(minute) / 60.0)))
            _arr.append(calc)

        return f"%{', '.join(map(str, _arr))}%"

    def __find_attribute__(self, _string: str, field: str):
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
        # find condition field
        for key, value in var.pattern_matching_attribute.items():
            # print(value)
            if re.search(value.get("pattern"), data_condition["str_a"]):
                data_condition["ac"].append(value.get("attribute"))
                # find data
                data = []
                if key == "data terbaru":
                    data.append(value.get("data"))
                elif key == "tanggal dikeluarkan":
                    date = re.search(value.get("data"), data_condition["str_a"]).group()
                    data.append(f"'{datetime.strptime(date.__str__(), '%d-%m-%Y').date()}'")
                elif key == "lintang":
                    search = re.search(value.get("data"), data_condition['str_a'])
                    if search:
                        data.append(f"'{self.__format_coordinates__(search.group().__str__())}'")
                else:
                    re_value = re.search(value.get("data"), data_condition["str_a"])
                    if re_value:
                        for result in re_value.groups():
                            if result is not None:
                                data.append(result)
                data_condition["d"].append(data)
                # find operator:
                # print(value.get('default_operator'))
                operator = ""
                if value.get("default_operator") is None:
                    for op_key, op_val in var.operator.items():
                        if op_val not in data_condition["op"]:
                            if re.search(op_key, data_condition["str_a"]):
                                operator = op_val
                                break
                else:
                    operator = value.get("default_operator")
                data_condition["op"].append(operator)
        return selected_field, data_condition["ac"], data_condition["op"], data_condition["d"]

    def __pattern_matching_input__(self, Pattern: dict, _string: str, rule: str):
        for field in Pattern:
            match = re.findall(Pattern.get(field), _string)
            if len(match) > 0:
                print(f'Parsing -> {rule}')
                return self.__find_attribute__(_string, field)

        self.rule_error = True
        self.rule = rule
        return False

    def get_error_status(self):
        return self.default_error, self.rule_error, self.rule

    def parsing_input(self, _string: str):
        if re.match(var.TAMPILKAN, _string):
            rule = "aturan 1"
            return self.__pattern_matching_input__(var.PATTERN_RULE_TAMPILKAN, _string, rule)

        if re.match(var.BERAPA, _string):
            rule = "aturan 2"
            return self.__pattern_matching_input__(var.PATTERN_RULE_BERAPA, _string, rule)

        if re.match(var.DIMANA, _string):
            rule = "aturan 3"
            return self.__pattern_matching_input__(var.PATTERN_RULE_DIMANA, _string, rule)

        if re.match(var.KAPAN, _string):
            rule = "aturan 4"
            return self.__pattern_matching_input__(var.PATTERN_RULE_KAPAN, _string, rule)

        if re.match(var.APA, _string):
            rule = "aturan 5"
            return self.__pattern_matching_input__(var.PATTERN_RULE_APA, _string, rule)

        if re.match(var.ARAH, _string):
            rule = "aturan 6"
            return self.__pattern_matching_input__(var.PATTERN_RULE_ARAH, _string, rule)

        self.default_error = True
        return False
