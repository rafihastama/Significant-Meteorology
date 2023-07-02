class Translator:
    def __init__(self, _selected_field, _selected_attribute_condition, _operator_condition, _data):
        self.sf = _selected_field
        self.sac = _selected_attribute_condition
        self.op = _operator_condition
        self.d = _data

    def __format_condition__(self):
        _str = ""
        if len(self.sac) > 1 and len(self.op) > 1 and len(self.d) > 1:
            n = (len(self.sac)+len(self.op)+len(self.d))/3
            for i in range(int(n)):
                if self.sac[0] == 'polygon':
                    if i == 0:
                        _str += f"{self.sac[i]} {self.op[i]} '{self.d[i]}' AND "
                    else:
                        _str += f"{self.sac[i]}{self.op[i]}{self.d[i]} AND "
                else:
                    _str += f"{self.sac[i]} {self.op[i]} {self.d[i]} AND "
        else:
            return f"{self.sac[0]}{self.op[0]}{self.d[0]}"

        return _str[:len(_str)-5]

    def translate_input_into_query(self):
        if 'from_valid_date' in self.sac:
            __selected_field = ''.join(map(str, self.sf))
            __operator = ''.join(map(str, self.op))
            if self.d[0][:2] > self.d[1][:2]:
                return f"SELECT {__selected_field} FROM extracted_sigmet WHERE " \
                       f"((({self.sac[0]} >= '{self.d[0]}' OR ({self.sac[0]} > '00:00:00' AND {self.sac[0]} < '{self.d[1]}')) " \
                       f"AND ({self.sac[1]} >= '00:00:00' AND {self.sac[1]} < '{self.d[1]}')) OR " \
                       f"(({self.sac[0]} >= '{self.d[0]}' OR ({self.sac[0]} > '00:00:00' AND {self.sac[0]} < '{self.d[1]}')) " \
                       f"AND ({self.sac[1]} >= '00:00:00' AND {self.sac[1]} < '{self.d[1]}'))) AND {self.sac[2]}{__operator}{self.d[2]}"

            return f"SELECT {__selected_field} FROM extracted_sigmet WHERE (" \
                   f"{self.sac[0]} BETWEEN TIME '{self.d[0]}' AND TIME '{self.d[1]}' " \
                   f"AND {self.sac[1]} BETWEEN TIME '{self.d[0]}' AND TIME '{self.d[1]}') " \
                   f"AND {self.sac[2]}{__operator}{self.d[2]}"

        __selected_field = ', '.join(map(str, self.sf))
        return f"SELECT {__selected_field} FROM extracted_sigmet WHERE {self.__format_condition__()}"
