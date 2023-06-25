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
                raise Exception(err.__str__())

    def search(self, query):
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print("Something went wrong when searching data: {}".format(err))
        finally:
            self.cursor.close()

    def close_connection(self):
        self.db.close()
