import re

patterns = {
    "sigmet_code": r"(SIGMET (\d{2}))",
    "valid_date": r"(VALID (\d{6}\/\d{6}))",
    "flight_information": r"(JAKARTA|UJUNG PANDANG)",
    "mountain": r"((MT) (\w{3,10}))",
    "mountain_pos": r"((PSN) ((S|N|E)(\d{4,5}) (S|N|E)(\d{4,5})))",
    "observer_at": r"(\d{4,5}Z)",
    "polygon": r"((N|S|E)(\s)(\d{4,5}))|((N|S|E)(\d{4,5}))",
    "flight_level": r"(FL(\d{3,}))",
    "va_movement": r"(MOV\s\w{1,})",
    "va_speed": r"(\d{2,}KT)",
    "insensitivity": r"(WKN|NC|INTSF)",
    "status": r"(CNL)",
    "sigmet_cnl_code": "(CNL SIGMET (\d{2}))",
    "sigmet_cnl_valid_date": r"(VALID (\d{6}\/\d{6}))",
}

data = ['WAAF SIGMET 14 VALID 101657/101710 WAAA- WAAF UJUNG PANDANG FIR CNL SIGMET 07 101126/101710=',
        'WAAF SIGMET 02 VALID 090336/090850 WAAA- WAAF UJUNG PANDANG FIR VA ERUPTION MT SEMERU PSN S0806 E11255 VA CLD OBS AT 0250Z SFC/FL130 MOV W 10KT WKN=',
        'WAAF SIGMET 06 VALID 091229/091729 WAAA- WAAF UJUNG PANDANG FIR VA ERUPTION MT DUKONO PSN N0142 E12754 VA CLD OBS AT 1100Z WI N0136 E12754 - N0148 E12740 - N0205 E12754 - N 0154 E12811 - N0136 E12754 SFC/FL070 MOV N 05KT NC=',
        'WIIF SIGMET 14 VALID 091425/091915 WIII- WIIF JAKARTA FIR VA ERUPTION MT KRAKATAU PSN S0606 E10525 VA CLD OBS AT 1350Z WI S0607 E10527 - S0619 E10455 - S0609 E10438 - S0557 E10452 - S0604 E10526 - S0607 E10527 SFC/FL050 MOV W 10KT NC=']

for d in data:
    print(d)
    for pattern in patterns:
        try:
            res = re.findall(patterns.get(pattern), d)
            if pattern == "polygon":
                if len(res) < 1:
                    continue

            print(pattern, "->", res)
        except AttributeError:
            print('')

    break