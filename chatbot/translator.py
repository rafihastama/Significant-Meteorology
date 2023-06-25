import re
from var import var
from decimal import Decimal


class Translator:
    def build_query(self, rule, field, res: list = None):
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
                    return f"SELECT * FROM extracted_sigmet WHERE CAST({_field} AS SIGNED) > 0 AND CAST({_field} AS SIGNED) {condition} {number} AND status = ''"
                case "flight level":
                    _field = "flight_level" if "fl" == field else "flight_level"
                    return f"SELECT * FROM extracted_sigmet WHERE {_field} = '{res[0]}' AND status = ''"
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
                    return f"SELECT * FROM extracted_sigmet WHERE polygon_extracted LIKE '%{_str}%' AND status = ''"
                case "valid":
                    if int(res[0][:2]) > int(res[1][:2]):
                        return f"SELECT * FROM extracted_sigmet WHERE from_valid_date >= '{res[0]}' " \
                               f"AND (to_valid_date >= '00:00' and to_valid_date <= '{res[1]}') AND status = ''"

                    return f"SELECT * FROM extracted_sigmet WHERE from_valid_date >= '{res[0]}' " \
                           f"AND (to_valid_date >= '{res[0]}' and to_valid_date <= '{res[1]}') AND status = ''"
                case "penyebaran abu vulkanik":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT polygon_extracted FROM extracted_sigmet WHERE status = ''"

                    arr = res[0].split(" ")
                    field = "sigmet_code"
                    cond = arr[1]
                    return f"SELECT polygon_extracted FROM extracted_sigmet WHERE {field} = '{cond}' AND status = ''"
                case _:
                    _str = ', '.join(map(str, field))

                    if "seluruh field" in _str:
                        return f"SELECT * FROM extracted_sigmet WHERE status = ''"

                    return f"SELECT {_str[:len(_str)]} FROM extracted_sigmet WHERE status = ''"

        if rule == "aturan 2":
            match field:
                case "valid":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT valid_date FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT valid_date FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case "ketinggian abu vulkanik":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT feet, meter FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT feet, meter FROM extracted_sigmet where sigmet_code='{_str[1]}'"
                case "kecepatan abu vulkanik":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT va_speed FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT va_speed FROM extracted_sigmet where sigmet_code='{_str[1]}'"

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

        if rule == "aturan 6":
            match field:
                case "arah abu vulkanik":
                    if res[0] == "info sigmet terkini" or res[0] == "info sigmet terbaru":
                        return f"SELECT va_movement FROM extracted_sigmet"

                    _str = res[0].split(" ")
                    return f"SELECT va_movement FROM extracted_sigmet where sigmet_code='{_str[1]}'"