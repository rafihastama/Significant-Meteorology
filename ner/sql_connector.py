import json
import mysql.connector


class sql:
    def __init__(self):
        self.cursor = None
        with open('connection.json') as data:
            conn_data = json.load(data)
            try:
                self.db = mysql.connector.connect(
                    user=conn_data['user'],
                    password=conn_data['password'],
                    host=conn_data['host'],
                    port=conn_data['port'],
                    database=conn_data['database'],
                    ssl_ca=conn_data['ssl_ca'],
                    ssl_disabled=conn_data['ssl_disabled'])
            except mysql.connector.Error as err:
                self.status = False
            else:
                self.status = True

    def check_connection(self):
        return self.status

    def insert(self, data):
        self.cursor = self.db.cursor()
        try:
            query = "INSERT INTO extracted_sigmet (release_date, release_time, sigmet, status, " \
                    "sigmet_code, cancelation_sigmet_code, valid_date, valid_date_sigmet_cancellation, flight_information, mountain, " \
                    "mountain_pos, observed_at, polygon, polygon_extracted, flight_level, feet, meter, va_movement, va_speed, intensitivity)" \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, data)
            self.db.commit()
            # print(self.cursor.rowcount, " records inserted.")
        except mysql.connector.Error as err:
            print("Something went wrong when inserting data: {}".format(err))
        finally:
            self.cursor.close()

    def fetch_data(self, table: str):
        self.cursor = self.db.cursor()
        try:
            query = f"SELECT * FROM {table} WHERE extracted='0'"
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print("Something went wrong when inserting data: {}".format(err))
        finally:
            self.cursor.close()

    def update_sigmet_data(self, _id):
        self.cursor = self.db.cursor()
        try:
            query = f"UPDATE sigmet_data SET extracted='1' WHERE id='{_id}'"
            self.cursor.execute(query)
            self.db.commit()
        except mysql.connector.Error as err:
            print("Something went wrong when updating data: {}".format(err))
        finally:
            self.cursor.close()

    def update_cancellation_sigmet(self, data: list):
        self.cursor = self.db.cursor()
        try:
            for d in data:
                query = f"UPDATE extracted_sigmet SET status = 'Dibatalkan' WHERE valid_date = '{d}'"
                self.cursor.execute(query)
                self.db.commit()
                # print(self.cursor.rowcount, " records updated.")
        except mysql.connector.Error as err:
            print("Something went wrong when updating data: {}".format(err))
        finally:
            self.cursor.close()

    def close_conn(self):
        self.db.close()
