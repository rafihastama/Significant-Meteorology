import re
from decimal import Decimal
from var import var


class Translator:
    def translate_input(self, rule, field, res: list = None):
        """
        function untuk ngebuat query berdasarkan hasil dari parsing
        input text

        :param rule: aturan
        :param field: field di db
        :param res: result dari hasil regex
        :return: query
        """

        if rule == "aturan 1":
            match field:
                case "ketinggian":
                    number = res[1]
                    condition = ">" if "lebih dari" == res[0] else "<"
                    _field = "feet" if "kaki" == res[2] else "meter"

                    if res[3] == "info sigmet terkini" or res[3] == "info sigmet terbaru":
                        return f"SELECT * FROM extracted_sigmet WHERE CAST({_field} AS SIGNED) > 0 AND CAST({_field} AS SIGNED) {condition} {number} "

                    return f"SELECT * FROM extracted_sigmet WHERE (CAST({_field} AS SIGNED) > 0 AND CAST({_field} AS SIGNED) {condition} {number}) AND sigmet_code={res[3].split(' ')[1]} "
                case "flight level":
                    _field = "flight_level" if "fl" == field else "flight_level"
                    return f"SELECT * FROM extracted_sigmet WHERE {_field} = '{res[0]}' "
                case "lintang":
                    arr = ''.join(map(str, res)).split(" ")
                    _arr = []
                    for i in range(len(arr)):
                        print(arr[i])
                        degree = arr[i][1:len(arr[i]) - 2]
                        minute = arr[i][len(arr[i]) - 2:]
                        calc = Decimal(degree) + (Decimal(minute) / 60)
                        _format = f"{round(calc, 2)}\N{DEGREE SIGN} " \
                                  f"{'Utara' if 'n' in arr[i] else 'Timur' if 'e' in arr[i] else 'Selatan' if 's' in arr[i] else 'Barat'}"
                        _arr.append(_format)
                    _str = ' '.join(map(str, _arr))
                    return f"SELECT * FROM extracted_sigmet WHERE polygon_extracted LIKE '%{_str}%' "
                case "valid":
                    if int(res[0][:2]) > int(res[1][:2]):
                        return f"SELECT * FROM extracted_sigmet WHERE from_valid_date >= '{res[0]}' " \
                               f"AND (to_valid_date >= '00:00' and to_valid_date <= '{res[1]}') "

                    return f"SELECT * FROM extracted_sigmet WHERE from_valid_date >= '{res[0]}' " \
                           f"AND (to_valid_date >= '{res[0]}' and to_valid_date <= '{res[1]}') "
                case "penyebaran abu vulkanik":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT polygon_extracted FROM extracted_sigmet "

                    arr = res[0].split(" ")
                    field = "sigmet_code"
                    cond = arr[1]
                    return f"SELECT polygon_extracted FROM extracted_sigmet WHERE {field} = '{cond}'"
                case _:
                    if len(field) <= 0:
                        return 0

                    _str = ', '.join(map(str, field))

                    if "seluruh field" in _str:
                        return f"SELECT * FROM extracted_sigmet "

                    return f"SELECT {_str[:len(_str)]} FROM extracted_sigmet "

        if rule == "aturan 2":
            match field:
                case "valid":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT valid_date FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT valid_date FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case "ketinggian abu vulkanik":
                    print(res, field)

                    selected_field = []
                    condition = []
                    data = []

                    # find selected field
                    for key_attribute in var.attribute:
                        if isinstance(key_attribute, tuple):
                            for key_data in key_attribute:
                                if re.match(key_data, field):
                                    selected_field.append(var.attribute.get(key_attribute))
                        else:
                            if re.match(key_attribute, field):
                                if isinstance(var.attribute.get(key_attribute), dict):
                                    for _, value in var.attribute.get(key_attribute).items():
                                        selected_field.append(value)
                                else:
                                    selected_field.append(var.attribute.get(key_attribute))

                    print(selected_field)

                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT feet, meter FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT feet, meter FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case "kecepatan abu vulkanik":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT va_speed FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT va_speed FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case _:
                    print('Kalimat yang diinputkan tidak dapat diproses')

        if rule == "aturan 3":
            match field:
                case "lokasi gunung":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT mountain, mountain_pos FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT mountain, mountain_pos FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case "lokasi flight information":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT flight_information, observed_at FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT flight_information, observed_at FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case "penyebaran abu vulkanik":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT polygon_extracted FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT polygon_extracted FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case _:
                    print('Kalimat yang diinputkan tidak dapat diproses')

        if rule == "aturan 4":
            match field:
                case "dikeluarkan":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT release_date, release_time FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT  release_date, release_time FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case "diobservasi":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT observed_at FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT release_date, observed_at FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case _:
                    print('Kalimat yang diinputkan tidak dapat diproses')

        if rule == "aturan 5":
            match field:
                case "status":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT status FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT status FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case "intesitas abu vulkanik":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT intensitivity FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT intensitivity FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case _:
                    print('Kalimat yang diinputkan tidak dapat diproses')

        if rule == "aturan 6":
            match field:
                case "arah abu vulkanik":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT va_movement FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT va_movement FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case _:
                    print('Kalimat yang diinputkan tidak dapat diproses')

    def translate_input_test(self, rule, field, res: list = None):
        """
        function untuk ngebuat query berdasarkan hasil dari parsing
        input text

        :param rule: aturan
        :param field: field di db
        :param res: result dari hasil regex
        :return: query
        """

        if rule == "aturan 1":
            match field:
                case "ketinggian":
                    number = res[1]
                    condition = ">" if "lebih dari" == res[0] else "<"
                    _field = "feet" if "kaki" == res[2] else "meter"

                    if res[3] == "info sigmet terkini" or res[3] == "info sigmet terbaru":
                        return f"SELECT * FROM extracted_sigmet WHERE CAST({_field} AS SIGNED) > 0 AND CAST({_field} AS SIGNED) {condition} {number} "

                    return f"SELECT * FROM extracted_sigmet WHERE (CAST({_field} AS SIGNED) > 0 AND CAST({_field} AS SIGNED) {condition} {number}) AND sigmet_code={res[3].split(' ')[1]} "
                case "flight level":
                    _field = "flight_level" if "fl" == field else "flight_level"
                    return f"SELECT * FROM extracted_sigmet WHERE {_field} = '{res[0]}' "
                case "lintang":
                    arr = ''.join(map(str, res)).split(" ")
                    _arr = []
                    for i in range(len(arr)):
                        print(arr[i])
                        degree = arr[i][1:len(arr[i]) - 2]
                        minute = arr[i][len(arr[i]) - 2:]
                        calc = Decimal(degree) + (Decimal(minute) / 60)
                        _format = f"{round(calc, 2)}\N{DEGREE SIGN} " \
                                  f"{'Utara' if 'n' in arr[i] else 'Timur' if 'e' in arr[i] else 'Selatan' if 's' in arr[i] else 'Barat'}"
                        _arr.append(_format)
                    _str = ' '.join(map(str, _arr))
                    return f"SELECT * FROM extracted_sigmet WHERE polygon_extracted LIKE '%{_str}%' "
                case "valid":
                    if int(res[0][:2]) > int(res[1][:2]):
                        return f"SELECT * FROM extracted_sigmet WHERE from_valid_date >= '{res[0]}' " \
                               f"AND (to_valid_date >= '00:00' and to_valid_date <= '{res[1]}') "

                    return f"SELECT * FROM extracted_sigmet WHERE from_valid_date >= '{res[0]}' " \
                           f"AND (to_valid_date >= '{res[0]}' and to_valid_date <= '{res[1]}') "
                case "penyebaran abu vulkanik":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT polygon_extracted FROM extracted_sigmet "

                    arr = res[0].split(" ")
                    field = "sigmet_code"
                    cond = arr[1]
                    return f"SELECT polygon_extracted FROM extracted_sigmet WHERE {field} = '{cond}'"
                case _:
                    if len(field) <= 0:
                        return 0

                    _str = ', '.join(map(str, field))

                    if "seluruh field" in _str:
                        return f"SELECT * FROM extracted_sigmet "

                    return f"SELECT {_str[:len(_str)]} FROM extracted_sigmet "

        if rule == "aturan 2":
            match field:
                case "valid":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT valid_date FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT valid_date FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case "ketinggian abu vulkanik":
                    print(res, field)

                    selected_field = []
                    condition = []
                    data = []

                    # find selected field
                    for key_attribute in var.attribute:
                        if isinstance(key_attribute, tuple):
                            for key_data in key_attribute:
                                if re.match(key_data, field):
                                    selected_field.append(var.attribute.get(key_attribute))
                        else:
                            if re.match(key_attribute, field):
                                if isinstance(var.attribute.get(key_attribute), dict):
                                    for _, value in var.attribute.get(key_attribute).items():
                                        selected_field.append(value)
                                else:
                                    selected_field.append(var.attribute.get(key_attribute))

                    print(selected_field)

                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT feet, meter FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT feet, meter FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case "kecepatan abu vulkanik":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT va_speed FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT va_speed FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case _:
                    print('Kalimat yang diinputkan tidak dapat diproses')

        if rule == "aturan 3":
            match field:
                case "lokasi gunung":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT mountain, mountain_pos FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT mountain, mountain_pos FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case "lokasi flight information":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT flight_information, observed_at FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT flight_information, observed_at FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case "penyebaran abu vulkanik":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT polygon_extracted FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT polygon_extracted FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case _:
                    print('Kalimat yang diinputkan tidak dapat diproses')

        if rule == "aturan 4":
            match field:
                case "dikeluarkan":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT release_date, release_time FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT  release_date, release_time FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case "diobservasi":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT observed_at FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT release_date, observed_at FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case _:
                    print('Kalimat yang diinputkan tidak dapat diproses')

        if rule == "aturan 5":
            match field:
                case "status":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT status FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT status FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case "intesitas abu vulkanik":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT intensitivity FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT intensitivity FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case _:
                    print('Kalimat yang diinputkan tidak dapat diproses')

        if rule == "aturan 6":
            match field:
                case "arah abu vulkanik":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT va_movement FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT va_movement FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case _:
                    print('Kalimat yang diinputkan tidak dapat diproses')
