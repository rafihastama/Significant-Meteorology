import json
import re
import gc
import sys
from datetime import datetime
import sql_connector as conn


def knot_conversion(speed):
    return "{:.2f}".format(speed * 1.852)


def main():
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

    db = conn.sql()  # db

    if db.check_connection():
        cnl_sigmet_data = []  # List of canceled SIGMET data.
        waaf_data = db.fetch_data("sigmet_data")  # fetch data
        if len(waaf_data) > 0:
            for wd in waaf_data:
                print(f"{wd[3]} === {wd[0]}")
                insert_data = [wd[1], wd[2], wd[3]]
                _cnl = 0
                for pattern in patterns:
                    res = re.findall(patterns.get(pattern), wd[3], flags=re.A)
                    # status
                    if pattern == "status":
                        insert_data.append('')
                        if len(res) > 0:
                            _cnl = 1
                    # sigmet code
                    if pattern == "sigmet_code":
                        insert_data.append(res[0])
                        if _cnl:
                            insert_data.append(res[1])
                        else:
                            insert_data.append('')
                    # valid date
                    if pattern == "valid_date":
                        data = res[0].__str__().split("/")
                        _date = f"Tanggal {data[0][:2]}, {data[0][2:4]}:{data[0][4:]} - {data[1][2:4]}:{data[1][4:]}"
                        insert_data.append(_date)
                    # valid date sigmet cancellation
                    if pattern == "valid_date_sigmet_cancellation":
                        if len(res) > 0:
                            data_cnl = res[0].__str__().split("/")
                            _date_cnl = f"Tanggal {data_cnl[0][:2]}, {data_cnl[0][2:4]}:{data_cnl[0][4:]} - {data_cnl[1][2:4]}:{data_cnl[1][4:]}"
                            insert_data.append(_date_cnl)
                            cnl_sigmet_data.append(_date_cnl)
                        else:
                            insert_data.append('')
                    # flight information
                    if pattern == "flight_information":
                        insert_data.append(res[0])
                    # mountain
                    if pattern == "mountain":
                        if _cnl:
                            insert_data.append('')
                        else:
                            insert_data.append(res[0])
                    # mountain pos
                    if pattern == "mountain_pos":
                        if _cnl:
                            insert_data.append('')
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
                            insert_data.append(_str)
                    # observed at
                    if pattern == "observed_at":
                        if _cnl:
                            insert_data.append('')
                        else:
                            _format = f"{res[0][:2]}:{res[0][2:4]}"
                            insert_data.append(_format)
                    # polygon
                    if pattern == "polygon":
                        if _cnl:
                            insert_data.extend(['', ''])
                        else:
                            if len(res) > 2:
                                _data = res[2:]
                                _polygon_calculated = []
                                _polygon_formated = []
                                for i in range(len(_data)):
                                    _data[i] = _data[i].replace(" ", "")
                                    degree = _data[i][1:len(_data[i]) - 2]
                                    minute = _data[i][len(_data[i]) - 2:]
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
                                insert_data.extend([_str_pc[:len(_str_pc) - 2], _str_pf[:len(_str_pf) - 3]])
                            else:
                                insert_data.extend(['', ''])
                    # flight level
                    if pattern == "flight_level":
                        if _cnl:
                            insert_data.extend(['', '', ''])
                        else:
                            if len(res) > 0:
                                with open('flight_level.json') as file:
                                    json_data = json.load(file)
                                    for jd in json_data:
                                        if str(jd['Flight Level']) == res[0]:
                                            feet = jd['Feet']
                                            meter = jd['Meter']
                                    insert_data.extend([res[0], feet, meter])
                            else:
                                insert_data.extend(['', '', ''])
                    # va movement
                    if pattern == "va_movement":
                        if _cnl:
                            insert_data.append('')
                        else:
                            _str = "Selatan" if "S" in res[0] else "Timur" if "E" in res[0] else "Utara" if "N" in res[
                                0] else "Barat"
                            insert_data.append(_str)
                    # va speed
                    if pattern == "va_speed":
                        if _cnl:
                            insert_data.append('')
                        else:
                            if len(res) > 0:
                                speed = re.findall(r"\d{1,3}", res[0])
                                _str = f"{knot_conversion((float(speed[0])))} km/h"
                                insert_data.append(_str)
                            else:
                                insert_data.append('')
                    # intensitivity
                    if pattern == "intensitivity":
                        if _cnl:
                            insert_data.append('')
                        else:
                            if len(res) > 0:
                                _str = "Tidak ada perubahan" if "NC" in res[0] else "Melemah" if "WKN" in res[0] else "Intensif"
                                insert_data.append(_str)
                            else:
                                insert_data.append('')

                db.insert(data=insert_data)
                db.update_sigmet_data(wd[0])
                gc.collect()

            if len(cnl_sigmet_data) > 0:
                db.update_cancellation_sigmet(cnl_sigmet_data)

        db.close_conn()


if __name__ == "__main__":
    main()
