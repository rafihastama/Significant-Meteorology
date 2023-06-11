import re


def knot_conversion(speed):
    return "{:.2f}".format(speed * 1.852)


def main():
    patterns = {
        "status": r"(CNL)",
        "sigmet_code": r"SIGMET\s(\d{2})",
        "valid_date": r"VALID\s(\d{6}\/\d{6})",
        "flight_information": r"(JAKARTA|UJUNG PANDANG)",
        "mountain": r"MT\s(\w{3,10})",
        "mountain_pos": r"PSN\s([NSEW]\d{4,5}\s[NSEW]\d{4,5})",
        # "mountain_pos": r"((PSN) ((S|N|E)(\d{4,5}) (S|N|E)(\d{4,5})))",
        "observed_at": r"(\d{4,5}Z)",
        "polygon": r"[NSE]\s\d{4,5}|[NSE]\d{4,5}",
        # "polygon": r"(?s)((N|S|E)(\s)(\d{4,5}))|((N|S|E)(\d{4,5}))",
        "flight_level": r"FL(\d{3,})",
        "va_movement": r"MOV\s(\w{1,})",
        "va_speed": r"(\d{1,}KT)",
        "intensitivity": r"(WKN|NC|INTSF)",
        # "sigmet_cnl_valid_date": r"VALID\s\d{6}\/\d{6}",
    }

    waaf_data = ['WAAF SIGMET 14 VALID 101657/101710 WAAA- WAAF UJUNG PANDANG FIR CNL SIGMET 07 101126/101710=',
            'WAAF SIGMET 02 VALID 090336/090850 WAAA- WAAF UJUNG PANDANG FIR VA ERUPTION MT SEMERU PSN S0806 E11255 VA CLD OBS AT 0250Z SFC/FL130 MOV W 10KT WKN=',
            'WAAF SIGMET 06 VALID 091229/091729 WAAA- WAAF UJUNG PANDANG FIR VA ERUPTION MT DUKONO PSN N0142 E12754 VA CLD OBS AT 1100Z WI N0136 E12754 - N0148 E12740 - N0205 E12754 - N 0154 E12811 - N0136 E12754 SFC/FL070 MOV N 05KT NC=',
            'WIIF SIGMET 14 VALID 091425/091915 WIII- WIIF JAKARTA FIR VA ERUPTION MT KRAKATAU PSN S0606 E10525 VA CLD OBS AT 1350Z WI S0607 E10527 - S0619 E10455 - S0609 E10438 - S0557 E10452 - S0604 E10526 - S0607 E10527 SFC/FL050 MOV W 10KT NC=']

    for wd in waaf_data:
        sql_data = ['','','']
        _cnl = 0
        for pattern in patterns:
            res = re.findall(patterns.get(pattern), wd[1], flags=re.A)
            # status
            if pattern == "status":
                if len(res) > 0:
                    _cnl = 1
                    sql_data.append('Dibatalkan')
                    print(f"{pattern} -> {res[0]}")
                else:
                    sql_data.append('')
                    print(f"{pattern} -> ")
            # sigmet code
            if pattern == "sigmet_code":
                sql_data.append(res[0])
                print(f"{pattern} -> {res[0]}")
                if _cnl:
                    sql_data.append(res[1])
                    print(f"cancelation_sigmet_code -> {res[1]}")
                else:
                    sql_data.append('')
                    print(f"cancelation_sigmet_code -> ")
            # valid date
            if pattern == "valid_date":
                data = res[0].__str__().split("/")
                # NOTE : tambah bulan dan tahun
                date = f"Tanggal {data[0][:2]}, {data[0][2:4]}:{data[0][4:]} - {data[1][2:4]}:{data[1][4:]}"
                sql_data.append(date)
                print(f"{pattern} -> {date}")
            # flight information
            if pattern == "flight_information":
                # sql_data += tuple(res[0])
                sql_data.append(res[0])
                print(f"{pattern} -> {res[0]}")
            # mountain
            if pattern == "mountain":
                if _cnl:
                    sql_data.append(r'')
                    print(f"{pattern} -> ")
                else:
                    sql_data.append(res[0])
                    print(f"{pattern} -> {res[0]}")
            # mountain pos
            if pattern == "mountain_pos":
                if _cnl:
                    sql_data.append(r'')
                    print(f"{pattern} -> ")
                else:
                    _data = res[0].__str__().split(" ")
                    # _str = []
                    # for dt in _data:
                    #     _str.append(
                    #         dt.replace(
                    #             "S" if "S" in dt
                    #             else "E" if "E" in dt
                    #             else "N" if "N" in dt
                    #             else "W",
                    #             "Lintang Selatan " if "S" in dt
                    #             else "Bujur Timur " if "E" in dt
                    #             else "Lintang Utara " if "N" in dt
                    #             else "Bujur Barat "
                    #         )
                    #     )
                    # _str = ' - '.join(map(str, _str))

                    _str = ""
                    for i in range(len(_data)):
                        if i % 2 == 0:
                            _str += f"{_data[i - 1]} {_data[i]} - "

                    _str = _str[:len(_str) - 3]

                    sql_data.append(_str)
                    print(f"{pattern} -> {_str}")
            # observed at
            if pattern == "observed_at":
                if _cnl:
                    sql_data.append(r'')
                    print(f"{pattern} -> ")
                else:
                    _format = f"{res[0][:2]}:{res[0][2:4]}"
                    sql_data.append(_format)
                    print(f"{pattern} -> {_format}")
            # polygon
            if pattern == "polygon":
                if _cnl:
                    sql_data.append(r'')
                    print(f"{pattern} -> ")
                else:
                    if len(res) > 2:
                        _data = res[2:]
                        _tmp = []
                        for dt in _data:
                            _tmp.append(
                                dt.replace(
                                    "S" if "S" in dt
                                    else "E" if "E" in dt
                                    else "N" if "N" in dt
                                    else "W",
                                    "Lintang Selatan " if "S" in dt
                                    else "Bujur Timur " if "E" in dt
                                    else "Lintang Utara " if "N" in dt
                                    else "Bujur Barat "
                                )
                            )
                        # format polygon here
                        # change _data to _tmp to see different result
                        _str = ""
                        for i in range(len(_data)):
                            if i % 2 == 0:
                                _str += f"{_data[i - 1]} {_data[i]} - "

                        _str = _str[:len(_str) - 3]
                        sql_data.append(_str)
                        print(f"{pattern} -> {_str}")
                    else:
                        sql_data.append('')
                        print(f"{pattern} -> ")
            # flight level
            if pattern == "flight_level":
                if _cnl:
                    sql_data.append(r'')
                    print(f"{pattern} -> ")
                else:
                    print(f"{pattern} -> {res[0]}")
                    sql_data.append(res[0])
            # va movement
            if pattern == "va_movement":
                if _cnl:
                    sql_data.append(r'')
                    print(f"{pattern} -> ")
                else:
                    _str = "Selatan" if "S" in res[0] else "Timur" if "E" in res[0] else "Utara" if "N" in res[
                        0] else "Barat"
                    sql_data.append(_str)
                    print(f"{pattern} -> {_str}")
            # va speed
            if pattern == "va_speed":
                if _cnl:
                    sql_data.append(r'')
                    print(f"{pattern} -> ")
                else:
                    speed = re.findall(r"\d{2,3}", res[0])
                    _str = f"{knot_conversion((float(speed[0])))} km/h"
                    sql_data.append(_str)
                    print(f"{pattern} -> {_str}")
            # intensitivity
            if pattern == "intensitivity":
                if _cnl:
                    sql_data.append(r'')
                    print(f"{pattern} -> ")
                else:
                    _str = "Tidak ada perubahan" if "NC" in res[0] else "Melemah" if "WKN" in res[0] else "Intensif"
                    sql_data.append(_str)
                    print(f"{pattern} -> {_str}")

        print(sql_data)


if __name__ == "__main__":
    main()
