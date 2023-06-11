import re
import sys
from datetime import datetime


def main():
    waaf_data = []

    with open("data.txt", 'r') as f:
        contents = f.readlines()

        for content in contents:
            if "WAAF" in content or "WIIF" in content:
                text_ = re.sub("([*])+", "", content).strip().lstrip()  # remove "*" and replace it with ''
                text_ = text_.replace("Received at ", '')  # remove "Received at" and replace it with ''
                d = [datetime.strptime(text_.strip()[:15], "%H:%M, %d/%m/%y"), text_[17:]]
                waaf_data.append(d)

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
        "sigmet_code": r"(SIGMET (\d{2}))",
        "valid_date": r"(VALID (\d{6}\/\d{6}))",
        "flight_information": r"(JAKARTA FIR|UJUNG PANDANG FIR)",
        "mountain": r"((MT) (\w{3,10}))",
        "mountain_pos": r"((PSN) ((S|N|E)(\d{4,5}) (S|N|E)(\d{4,5})))",
        "observer_at": r"(\d{4,5}Z)",
        "polygon": r"((N|S|E)(\s)(\d{4,5}))|((N|S|E)(\d{4,5}))",
        "flight_level": r"(FL(\d{3,}))",
        "va_movement": r"(MOV\s\w{1,})",
        "va_speed": r"(\d{2,}KT)",
        "insensitivity": r"(WKN|NC|INTSF)",
        "status": r"(CNL)",
        "sigmet_cnl_valid_date": r"(VALID (\d{6}\/\d{6}))",
    }

    i = 1

    for wd in waaf_data:
        print(wd[1])
        # for pattern in patterns:
        #     try:
        #         res = re.search(patterns.get(pattern), wd[1])
        #         if pattern == "polygon":
        #         # print(patterns.get(pattern))
        #             a = res.group().__str__()
        #             print(len(a))
        #             break
        #             if len(a) < 1:
        #                 continue
        #         # if res.group() is None:
        #         #     print('a')
        #         # else:
        #         print(pattern,"->",res.group())
        #     except AttributeError:
        #         print('')
        #
        # # if i == 10:
        # break

        # i += 1


if __name__ == "__main__":
    main()
