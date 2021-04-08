import psycopg2
import psycopg2.extras
import os
#DATABASE_URL = os.environ['DATABASE_URL']


class Database:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'itus'

    def connectToDatabase(self):
        #engine = psycopg2.connect(DATABASE_URL, sslmode='require')
        engine = psycopg2.connect(host=self.host, database=self.database)
        return engine

    @staticmethod
    def disconnectToDatabase(engine):
        engine.close()

    @staticmethod
    def getCursor(engine):
        cursor = engine.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return cursor

    @staticmethod
    def closeCursor(cursor):
        cursor.close()

    def initialiseStream(self):
        engine = self.connectToDatabase()
        cursor = self.getCursor(engine)
        return engine, cursor

    def uninitialiseStream(self, cursor, engine):
        self.closeCursor(cursor)
        self.disconnectToDatabase(engine)

    def pushDataSingle(self, sql, data):
        engine, cursor = self.initialiseStream()
        cursor.execute(sql, data)
        engine.commit()
        self.uninitialiseStream(cursor, engine)

    def pushDataMany(self, sql, data):
        engine, cursor = self.initialiseStream()
        cursor.executemany(sql, data)
        engine.commit()
        self.uninitialiseStream(cursor, engine)

    def pullData(self, sql, params=None):
        engine, cursor = self.initialiseStream()
        cursor.execute(sql, (params,))
        results = cursor.fetchall()
        self.uninitialiseStream(cursor, engine)
        return results
