import re
import xml.etree.ElementTree as ET
import lxml.etree as et
import pandas as pd
import json
import mysql.connector


def main():
    cnx = mysql.connector.connect(user="laqqueta", password="32241mysqlDB#", host="laqqueta.mysql.database.azure.com",
                                  port=3306, database="sigmet", ssl_ca="cert/certi.pem",
                                  ssl_disabled=False)
    try:
        cursor = cnx.cursor()

        data = ['2023-06-11', '10:48:00', 'WAAF SIGMET 14 VALID 111048/111130 WAAA- WAAF UJUNG PANDANG FIR CNL SIGMET 07 110544/111130=', '', '14', '07', 'Tanggal 11, 10:48 - 11:30', 'Tanggal 11, 05:44 - 11:30', 'UJUNG PANDANG', '', '', '', '', '', '', '', '', '', '', '']
        query = "INSERT INTO extracted_sigmet (release_date, release_time, sigmet, status, " \
                "sigmet_code, cancelation_sigmet_code, valid_date, valid_date_sigmet_cancellation, flight_information, mountain, " \
                "mountain_pos, observed_at, polygon, polygon_extracted, flight_level, feet, meter, va_movement, va_speed, intensitivity)" \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, data)
        cnx.commit()
        print("inserted")
        print(cnx.is_connected())
    except mysql.connector.Error as err:
        print("Something went wrong when inserting data: {}".format(err))


if __name__ == "__main__":
    main()
