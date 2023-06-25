from var import var
from translator import Translator
import re


class Parsing:
    def __init__(self):
        self._translator = Translator()
    
    def validate_input(self, Pattern: dict, _string: str, rule: str):
        found = 0
        _field = None
        _res = None
        for field in Pattern:
            match = re.findall(Pattern.get(field), _string)
            if len(match) > 0:
                _field = field
                found = 1
                if isinstance(match[0], tuple):
                    _res = list(filter(None, match[0]))
                else:
                    _res = list(filter(None, match))
                # translator
                query = self._translator.build_query(rule, _field, _res)
                print(f'query result -> {query}')
                return query

        if not found and rule == "aturan 1":
            _field = []
            for key, val in var.DATATABLE_TO_FIELD.items():
                if re.search(key, _string):
                    _field.append(val)
            # translator
            query = self._translator.build_query("aturan 1", _field)
            print(f'query result -> {query}')
            return query
        else:
            print("Query yang anda cari tidak ditemukan")
    
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