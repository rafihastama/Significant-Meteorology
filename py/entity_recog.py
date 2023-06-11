import re
import sys
from datetime import datetime


def knot_conversion(speed):
    return "{:.2f}".format(speed * 1.852)


def main():
    waaf_data = []

    with open("data.txt", 'r') as f:
        contents = f.readlines()
        # line = 1
        for content in contents:
            if "WAAF" in content or "WIIF" in content:
                text_ = re.sub("([*])+", "", content).strip().lstrip()  # remove "*" and replace it with ''
                text_ = text_.replace("Received at ", '')  # remove "Received at" and replace it with ''
                d = [datetime.strptime(text_.strip()[:15], "%H:%M, %d/%m/%y"), text_[17:]]
                waaf_data.append(d)

            #     if "VRB" in content or "FCST" in content:
            #         print(line)
            #         print(content)

            # line+=1

        waaf_data.sort(reverse=False)

    # format date
    for i in range(len(waaf_data)):
        waaf_data[i][0] = waaf_data[i][0].strftime("%H:%M, %d %B %Y")
        # print(waaf_data[i][1])

    # Tokenization and stop word removal
    # stop_word = open('stop_word.txt', 'r')

    # for i in range(len(waaf_data)):
    #     waaf_data[i][1] = waaf_data[i][1].split(" ")
    #     tmp_sw = []
    #     # stop word removal
    #     for j in range(len(waaf_data[i][1])):
    #         if waaf_data[i][1][j].lower() not in stop_word:
    #             tmp_sw.append(waaf_data[i][1][j])
    #
    #     waaf_data[i][1] = tmp_sw

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
        "va_movement": r"MOV\s(\w{1,})|MO\sV\s(\w{1,})|VRB",
        "va_speed": r"(\d{1,}KT)",
        "intensitivity": r"(WKN|NC|INTSF)",
        # "sigmet_cnl_valid_date": r"VALID\s\d{6}\/\d{6}",
    }

    n = 1

    for wd in waaf_data:
        # -------------
        # if n == 10:
        #     break
        # -------------
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
                date = f"{datetime.strftime(date, '%d %B %Y')}, {data[0][2:4]}:{data[0][4:]} - {data[1][2:4]}:{data[1][4:]}"
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
                    if res[0] == 'VRB':
                        print(f"{pattern} -> varies")
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
                    if len(res) > 0:
                        speed = re.findall(r"\d{1,3}", res[0])
                        _str = f"{knot_conversion((float(speed[0])))} km/h"
                        sql_data.append(_str)
                        print(f"{pattern} -> {_str}")
                    else:
                        sql_data.append('')
                        print(f"{pattern} -> None")

            # intensitivity
            if pattern == "intensitivity":
                if _cnl:
                    sql_data.append('')
                    print(f"{pattern} -> ")
                else:
                    if len(res) > 0:
                        _str = "Tidak ada perubahan" if "NC" in res[0] else "Melemah" if "WKN" in res[0] else "Intensif"
                        sql_data.append(_str)
                        print(f"{pattern} -> {_str}")
                    else:
                        sql_data.append('')
                        print(f"{pattern} -> None")

        print(sql_data)
        n += 1

    print(len(waaf_data))


if __name__ == "__main__":
    main()
