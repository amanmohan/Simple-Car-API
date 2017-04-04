import os
import json

import sqlite3


class DataOperations(object):

    def __init__(self):
        self.filename = 'tesla_db.db'
        self.car_list = ['ID','MAKE','YEAR','MODEL']
        self.rating_list = ['ID','Overall','interior','performance','reliablity','reviewedBy','technology']

    def create_connection(self):
        '''
        creating connection
        '''
        creating_tabel = self.create_tables()
        if creating_tabel:
            connection = sqlite3.connect(self.filename)
            return connection

    def close_connection(self,connection):
        '''
        close connection
        '''
        connection.commit()
        connection.close()
        return True

    def create_tables(self):
        '''
        creating cars table and ratings table
        '''
        file_in = os.path.isfile(self.filename)
        if file_in:
            return True
        connection = sqlite3.connect(self.filename)
        connection.execute('''CREATE TABLE CARS
                               (ID INT PRIMARY KEY     NOT NULL,
                               MAKE            TEXT    NOT NULL,
                               YEAR            TEXT    NOT NULL,
                               MODEL           TEXT    NOT NULL
                               );''')
        connection.execute('''CREATE TABLE RATINGS
                               (ID              INT    NOT NULL,
                               Overall          INT    NOT NULL,
                               interior         INT    NOT NULL,
                               performance      INT    NOT NULL,
                               reliablity       INT    NOT NULL,
                               reviewedBy       TEXT   NOT NULL,
                               technology       INT    NOT NULL,
                               FOREIGN KEY(ID) REFERENCES CARS(ID)
                               );''')

        connection.close()
        return True

    def push_car(self, car_info):
        '''
        push data into car table
        '''
        connection = self.create_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO CARS values (?, ?, ?, ?)", car_info)
        return self.close_connection(connection)

    def push_rating(self, rating_info):
        '''
        push data into ratings table
        '''
        connection = self.create_connection()
        cursor = connection.cursor()
        query = "INSERT INTO RATINGS values (?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(query, rating_info)
        return self.close_connection(connection)

    def modify_car(self, car_info):
        '''
        Update data into cars table
        '''
        connection = self.create_connection()
        cursor = connection.cursor()
        query = "UPDATE CARS set %s=(?), %s=(?), %s=(?) where %s=(?)" %tuple(self.car_list[::-1])
        cursor.execute(query, car_info[::-1])
        return self.close_connection(connection)

    def modify_rating(self, rating_info):
        '''
        Update data into ratings table
        '''
        connection = self.create_connection()
        cursor = connection.cursor()
        length = len(rating_info)
        query = "UPDATE RATINGS set " + "{:s} ".format('%s=(?)')*(length-1) + "where %s=(?)" \
                 %tuple(self.rating_list[::-1])
        cursor.execute(query, rating_info[::-1])
        return self.close_connection(connection)

    def give_cars(self):
        '''
        getting all cars
        '''
        connection = self.create_connection()
        cursor = connection.cursor()
        # Read all record
        sql = "SELECT * FROM CARS"
        cursor.execute(sql)
        results = cursor.fetchall()
        self.close_connection(connection)
        z = self.car_list
        results = [dict(zip(z,x)) for x in results]
        return results

    def give_ratings(self):
        '''
        getting all ratings
        '''
        connection = self.create_connection()
        cursor = connection.cursor()
        # Read all record
        sql = "SELECT * FROM RATINGS"
        cursor.execute(sql)
        results = cursor.fetchall()
        self.close_connection(connection)
        z = self.rating_list
        results = [dict(zip(z,x)) for x in results]
        return results

    def give_car(self, car_id):
        '''
        getting a car
        '''
        connection = self.create_connection()
        cursor = connection.cursor()
        # Read a record
        sql = "SELECT * FROM CARS WHERE ID = %d" %car_id
        cursor.execute(sql)
        result = cursor.fetchone()
        self.close_connection(connection)
        z = self.car_list
        if result:
            result = dict(zip(z,result))
        return result

    def give_rating(self, car_id):
        '''
        getting a rating
        '''
        connection = self.create_connection()
        cursor = connection.cursor()
        # Read a record
        sql = "SELECT * FROM RATINGS WHERE ID = %d" %car_id
        cursor.execute(sql)
        result = cursor.fetchone()
        self.close_connection(connection)
        z = self.rating_list
        if result:
            result = dict(zip(z,result))
        return result

    def return_new_id(self):
        '''
        getting new id
        '''
        connection = self.create_connection()
        cursor = connection.cursor()
        # Read a record
        sql = "SELECT MAX(ID) FROM CARS"
        cursor.execute(sql)
        result = cursor.fetchone()
        self.close_connection(connection)
        if result[0]:
            return result[0]
        return 0

    def remove_car(self, car_id):
        '''
        delete car row
        '''
        connection = self.create_connection()
        cursor = connection.cursor()
        # delete a record
        sql = "DELETE FROM CARS WHERE ID = %d" %car_id
        cursor.execute(sql)
        responce = self.close_connection(connection)
        return responce

    def remove_rating(self,car_id):
        '''
        delete rating row
        '''
        connection = self.create_connection()
        cursor = connection.cursor()
        # delete a record
        sql = "DELETE FROM RATINGS WHERE ID = %d" %car_id
        cursor.execute(sql)
        responce = self.close_connection(connection)
        return responce

d = DataOperations()
x = d.return_new_id()
z = d.give_car(1)
print x,z

'''
curl -i -H "Content-Type: application/json" -X POST -d '{"make":"as","model":"sad","year":"322"}' http://localhost:5000/api/cars
'''

'''
curl -i -H "Content-Type: application/json" -X PUT -d '{"ID":1,"make":"adssddsds","model":"dssad","year":"ds322"}' http://localhost:5000/api/cars/1
'''

'''
http://localhost:5000/api/cars
'''
