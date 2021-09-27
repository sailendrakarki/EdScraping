import cx_Oracle as Orcon
from cx_Oracle import DatabaseError


class Database:
    def __init__(self,conf):
        self._dns_tns = Orcon.makedsn(conf['HOST'],conf['PORT'],conf['SERVICE_NAME'])
        self._conn = Orcon.connect(conf['USER'], conf['PASSWORD'], self._dns_tns)
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self,commit= True):
        if commit:
            self.commit()
        self.connection.closer()
    
    def execute(self,sql,params=None):
        self.cursor.execute(sql,params or ())
    
    def fetchall(self):
        return self.cursor.fetchall()
    
    def fetchone(self):
        return self.cursor.fetchone()
    
    def query(self,sql,params=None):
        self.cursor.execute(sql,params or ())
        return self.fetchall()
    
