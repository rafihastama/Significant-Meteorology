class Translator:
    def __init__(self, _selected_field, _selected_attribute_condition, _operator_condition, _data, _data_length):
        self.sf = _selected_field
        self.sac = _selected_attribute_condition
        self.op = _operator_condition
        self.d = _data
        self.n = int(_data_length)

    def __format_condition__(self):
        _str = ""
        if len(self.sac) > 1 and len(self.op) > 1 and len(self.d) > 1:
            n = (len(self.sac) + len(self.op) + len(self.d)) / 3
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

        return _str[:len(_str) - 5]

    def __format__valid_date__(self, date: list, field: list):
        if date[0] > date[1]:
            return f"((({field[0]} >= '{date[0]}' OR ({field[0]} > '00:00:00' AND {field[0]} < '{date[1]}')) " \
                   f"AND ({field[1]} >= '00:00:00' AND {field[1]} < '{date[1]}')) OR " \
                   f"(({field[0]} >= '{date[0]}' OR ({date[0]} > '00:00:00' AND {field[0]} < '{date[1]}')) " \
                   f"AND ({field[1]} >= '00:00:00' AND {field[1]} < '{date[1]}')))"

        return f"({field[0]} BETWEEN TIME '{date[0]}' AND TIME '{date[1]}' " \
               f"AND {field[1]} BETWEEN TIME '{date[0]}' AND TIME '{date[1]}')"

    def translate_input_into_query(self):
        cond = ""
        for i in range(self.n):
            if self.op[i] == 'valid_date':
                cond += f"{self.__format__valid_date__(self.d[i], self.sac[i])} AND "
            else:
                cond += f"{self.sac[i]} {self.op[i]} {self.d[i][0]} AND "

        if len(self.sf) > 1:
            fields = ""
            for field in self.sf:
                fields += f"{field}, "
            return f"SELECT {fields[:len(fields)-2]} FROM extracted_sigmet WHERE {cond[:len(cond)-5]}"
        else:
            return f"SELECT {self.sf[0]} FROM extracted_sigmet WHERE {cond[:len(cond)-5]}"
