import re
import sys
import json
import sql_connector as conn
from datetime import datetime


# Note:
# FIX buat sigmet yang dibatalkan


def knot_conversion(speed):
    return "{:.2f}".format(speed * 1.852)


def main():
    waaf_data = []
    with open("data.txt", 'r') as f:
        contents = f.readlines()
        # line = 1
        for content in contents:
            if "WAAF" in content or "WIIF" in content:
                if "VRB" not in content or "FCST" not in content:
                    text_ = re.sub("([*])+", "", content).strip().lstrip()  # remove "*" and replace it with ''
                    text_ = text_.replace("Received at ", '')  # remove "Received at" and replace it with ''
                    d = [datetime.strptime(text_.strip()[:15], "%H:%M, %d/%m/%y"), text_[17:]]
                    waaf_data.append(d)

                    # if "CNL" in content:
                    #     # print(content)

        waaf_data.sort(reverse=False)

    # format date
    for i in range(len(waaf_data)):
        waaf_data[i][0] = waaf_data[i][0].strftime("%H:%M, %d %B %Y")
        # # print(waaf_data[i][1])

    patterns = {
        "status": r"(CNL)",
        "sigmet_code": r"SIGMET\s(\d{2})",
        "valid_date": r"VALID\s(\d{6}\/\d{6})",
        "valid_date_sigmet_cancellation": r"CNL\sSIGMET\s\d{2}\s(\d{6}\/\d{6})",
        "flight_information": r"(JAKARTA|UJUNG PANDANG)",
        "mountain": r"MT\s(\w{3,10})",
        "mountain_pos": r"PSN\s([NSEW]\d{4,5}\s[NSEW]\d{4,5})",
        "observed_at": r"(\d{4,5}Z)",
        "polygon": r"[NSE]\s\d{4,5}|[NSE]\d{4,5}",
        "flight_level": r"FL(\d{3,})",
        "va_movement": r"MOV\s(\w{1,})|MO\sV\s(\w{1,})|VRB",
        "va_speed": r"(\d{1,}KT)",
        "intensitivity": r"(WKN|NC|INTSF)",
    }
    # db
    db = conn.sql()
    n = 1
    for wd in waaf_data:
        # if n == 20:
        #     break
        # print(wd[1])
        date = datetime.strptime(wd[0], '%H:%M, %d %B %Y')
        sql_data = [datetime.strftime(date, "%Y-%m-%d"), datetime.strftime(date, "%H:%M:%S"), wd[1]]

        _cnl = 0
        for pattern in patterns:
            res = re.findall(patterns.get(pattern), wd[1], flags=re.A)
            # status
            if pattern == "status":
                if len(res) > 0:
                    _cnl = 1
                    sql_data.append('Dibatalkan')
                    # print(f"{pattern} -> {res[0]}")
                else:
                    sql_data.append('')
                    # print(f"{pattern} -> ")
            # sigmet code
            if pattern == "sigmet_code":
                sql_data.append(res[0])
                # print(f"{pattern} -> {res[0]}")
                if _cnl:
                    sql_data.append(res[1])
                    # print(f"cancelation_sigmet_code -> {res[1]}")
                else:
                    sql_data.append('')
                    # print(f"cancelation_sigmet_code -> ")
            # valid date
            if pattern == "valid_date":
                data = res[0].__str__().split("/")
                _date = f"Tanggal {data[0][:2]}, {data[0][2:4]}:{data[0][4:]} - {data[1][2:4]}:{data[1][4:]}"
                sql_data.append(_date)
                # print(f"{pattern} -> {_date}")
            # valid date sigmet cancellation
            if pattern == "valid_date_sigmet_cancellation":
                if len(res) > 0:
                    data = res[0].__str__().split("/")
                    _date = f"Tanggal {data[0][:2]}, {data[0][2:4]}:{data[0][4:]} - {data[1][2:4]}:{data[1][4:]}"
                    sql_data.append(_date)
                    # print(f'valid_date_sigmet_cancellation -> {_date}')
                else:
                    sql_data.append('')
            # flight information
            if pattern == "flight_information":
                # sql_data += tuple(res[0])
                sql_data.append(res[0])
                # print(f"{pattern} -> {res[0]}")
            # mountain
            if pattern == "mountain":
                if _cnl:
                    sql_data.append('')
                    # print(f"{pattern} -> ")
                else:
                    sql_data.append(res[0])
                    # print(f"{pattern} -> {res[0]}")
            # mountain pos
            if pattern == "mountain_pos":
                if _cnl:
                    sql_data.append('')
                    # print(f"{pattern} -> ")
                else:
                    _data = res[0].__str__().split(" ")
                    _tmp = []
                    for i in range(len(_data)):
                        _data[i] = _data[i].replace(" ", "")
                        degree = _data[i][1:len(_data[i]) - 2]
                        minute = _data[i][len(_data[i]) - 2:]
                        calc = float("{:.2f}".format(float(degree) + (float(minute) / 60.0)))
                        _format = f"{calc}\N{DEGREE SIGN} " \
                                  f"{'Utara' if 'N' in _data[i] else 'Timur' if 'E' in _data[i] else 'Selatan' if 'S' in _data[i] else 'Barat'}"

                        _tmp.append(_format)

                    _str = " ".join(map(str, _tmp))
                    sql_data.append(_str)
                    # print(f"{pattern} -> {_str}")
            # observed at
            if pattern == "observed_at":
                if _cnl:
                    sql_data.append('')
                    # print(f"{pattern} -> ")
                else:
                    _format = f"{res[0][:2]}:{res[0][2:4]}"
                    sql_data.append(_format)
                    # print(f"{pattern} -> {_format}")
            # polygon
            if pattern == "polygon":
                if _cnl:
                    sql_data.extend(['', ''])
                    # print(f"{pattern} -> ")
                else:
                    if len(res) > 2:
                        _data = res[2:]
                        _polygon_calculated = []
                        _polygon_formated = []
                        for i in range(len(_data)):
                            _data[i] = _data[i].replace(" ", "")
                            degree = _data[i][1:len(_data[i])-2]
                            minute = _data[i][len(_data[i])-2:]
                            calc = float("{:.2f}".format(float(degree) + (float(minute) / 60.0)))
                            _format = f"{calc}\N{DEGREE SIGN} " \
                                      f"{'Utara' if 'N' in _data[i] else 'Timur' if 'E' in _data[i] else 'Selatan' if 'S' in _data[i] else 'Barat'}"
                            _polygon_calculated.append(calc)
                            _polygon_formated.append(_format)

                        _str_pc = ""
                        _str_pf = ""
                        for i in range(len(_data)):
                            if i % 2 == 0:
                                _str_pc += f"[{_polygon_calculated[i]}, {_polygon_calculated[i - 1]}], "
                                _str_pf += f"{_polygon_formated[i]} {_polygon_formated[i - 1]} - "

                        _str_pc = _str_pc[:len(_str_pc) - 2]
                        _str_pf = _str_pf[:len(_str_pf) - 3]

                        sql_data.extend([_str_pc[:len(_str_pc) - 2], _str_pf[:len(_str_pf) - 3]])
                        # print(f"{pattern} -> {_str_pc}, {_str_pf}")
                    else:
                        sql_data.extend(['', ''])
                        # print(f"{pattern} -> ")
            # flight level
            if pattern == "flight_level":
                if _cnl:
                    sql_data.extend(['', '', ''])
                    # print(f"{pattern} -> ")
                else:
                    if len(res) > 0:
                        # feet, meter = None, None
                        with open('flight_level.json') as file:
                            json_data = json.load(file)
                            for jd in json_data:
                                if str(jd['Flight Level']) == res[0]:
                                    feet = jd['Feet']
                                    meter = jd['Meter']

                            # print(f"{pattern} -> {res[0]}, {feet}, {meter}")
                            sql_data.extend([res[0], feet, meter])
                    else:
                        sql_data.extend(['', '', ''])
            # va movement
            if pattern == "va_movement":
                if _cnl:
                    sql_data.append('')
                    # print(f"{pattern} -> ")
                else:
                    _str = "Selatan" if "S" in res[0] else "Timur" if "E" in res[0] else "Utara" if "N" in res[
                        0] else "Barat"
                    sql_data.append(_str)
                    # print(f"{pattern} -> {_str}")
            # va speed
            if pattern == "va_speed":
                if _cnl:
                    sql_data.append('')
                    # print(f"{pattern} -> ")
                else:
                    if len(res) > 0:
                        speed = re.findall(r"\d{1,3}", res[0])
                        _str = f"{knot_conversion((float(speed[0])))} km/h"
                        sql_data.append(_str)
                        # print(f"{pattern} -> {_str}")
                    else:
                        sql_data.append('')
                        # print(f"{pattern} -> None")
            # intensitivity
            if pattern == "intensitivity":
                if _cnl:
                    sql_data.append('')
                    # print(f"{pattern} -> ")
                else:
                    if len(res) > 0:
                        _str = "Tidak ada perubahan" if "NC" in res[0] else "Melemah" if "WKN" in res[0] else "Intensif"
                        sql_data.append(_str)
                        # print(f"{pattern} -> {_str}")
                    else:
                        sql_data.append('')
                        # print(f"{pattern} -> None")
        
        n += 1
        # print("50"*50)
        db.insert(data=sql_data)
        # if len(sql_data) <= 16:
        # print(sql_data)
        # print(len(sql_data))

    db.close_conn()


if __name__ == "__main__":
    main()
