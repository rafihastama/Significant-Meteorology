import mysql.connector


class sql:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sigmet"
    )

    def insert(self, data):
        cursor = self.db.cursor()
        try:
            query = "INSERT INTO extracted_sigmet (release_date, release_time, sigmet, status, " \
                    "sigmet_code, cancelation_sigmet_code, valid_date, valid_date_sigmet_cancellation, flight_information, mountain, " \
                    "mountain_pos, observed_at, polygon, polygon_extracted, flight_level, feet, meter, va_movement, va_speed, intensitivity)" \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, data)
            self.db.commit()
            print(cursor.rowcount, " records inserted.")
        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
        finally:
            cursor.close()

    def close_conn(self):
        self.db.close()
