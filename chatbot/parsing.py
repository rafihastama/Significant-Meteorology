from pattern_rule import var
from datetime import datetime
import re


class Parsing:
    def __init__(self):
        self.rule_error = None
        self.rule = None
        self.default_error = None

    def __format_coordinates__(self, coords: str, wind_dir: bool = False):
        arr = ''.join(map(str, coords)).split(" ")
        _arr = []
        _str_tmp = []
        for i in range(len(arr)):
            degree = arr[i][1:len(arr[i]) - 2]
            minute = arr[i][len(arr[i]) - 2:]
            calc = float("{:.2f}".format(float(degree) + (float(minute) / 60.0)))
            if wind_dir:
                _format = f"{calc}\N{DEGREE SIGN} " \
                          f"{'Utara' if 'N' in coords[i] else 'Timur' if 'E' in coords[i] else 'Selatan' if 'S' in coords[i] else 'Barat'}"
                _str_tmp.append(_format)

            _arr.append(calc)

        if wind_dir:
            return " ".join(map(str, _str_tmp))

        return f"%{', '.join(map(str, _arr))}%"

    def __find_attribute__(self, _string: str, field: str):
        selected_field = []  # selected attribute
        data_condition = {
            "str_b": "",  # string before where clause (condition)
            "str_a": "",  # string after where clause (condition)
            "con": "",  # value : where
            "ac": [],  # attribute for where clause
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
                    break
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
            match = re.search(value.get("pattern"), data_condition["str_a"])
            if match:
                # find attribute condition
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
                elif key == "status sigmet" \
                        or key == "flight information" \
                        or key == "mountain location" \
                        or key == "intensitivity":
                    _str = re.search(value.get("data"), data_condition["str_a"]).group()
                    data.append(f"'%{_str}%'")
                elif key == "mountain position":
                    search = re.search(value.get("data"), data_condition['str_a'])
                    if search:
                        data.append(f"'{self.__format_coordinates__(search.group().__str__(), wind_dir=True)}'")
                elif key == "volcanic ash movement":
                    _str = re.search(value.get("data"), data_condition["str_a"]).group()
                    data.append(f"'{_str}'")
                else:
                    re_value = re.search(value.get("data"), data_condition["str_a"])
                    if re_value:
                        for result in re_value.groups():
                            if result is not None:
                                data.append(result)
                data_condition["d"].append(data)
                # find operator
                operator_str = match.group()
                operator = ""
                if value.get("default_operator") is None:
                    for op_key, op_val in var.operator.items():
                        if re.search(op_key, operator_str):
                            operator = op_val
                            break
                else:
                    operator = value.get("default_operator")
                data_condition["op"].append(operator)

        # check if in str b have pattern for current date
        for key, value in var.pattern_matching_attribute.items():
            if key == "data terbaru" and re.search(value.get("pattern"), data_condition["str_b"]):
                data_condition["ac"].append(value.get("attribute"))
                data_condition["op"].append(value.get("default_operator"))
                data_condition["d"].append([value.get("data")])

        n = (len(data_condition["ac"]) + len(data_condition["op"]) + len(data_condition["d"])) / 3
        return selected_field, data_condition["ac"], data_condition["op"], data_condition["d"], n

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
            print('a')
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
