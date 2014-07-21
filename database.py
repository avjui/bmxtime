import sqlite3
from logger import Log

log = Log()
class Database():

    def __init__(self):
        self.name = 'timebase.db'
        self.connection = sqlite3.connect(self.name, timeout=20)        
        self.CeckDatabase()
        
    def CeckDatabase(self):

        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Fahrer (FahrerNR INTEGER, Nachname TEXT, Vorname TEXT, Datum TEXT, Klasse TEXT ) ')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS Zeiten (FahrerNR INTEGER, Zwischenzeit1 TEXT, Zwischenzeit2 TEXT, Endzeit TEXT) ')
        self.connection.commit()
        self.cursor.close()

    def AddData(self, table, columnlist1):

        self.cursor = self.connection.cursor()
        sql = "INSERT INTO '%s'(FahrerNr, Nachname, Vorname, Datum, Klasse)VALUES (%d, '%s', '%s', '%s', '%s')"%(table, columnlist1[0], columnlist1[1], columnlist1[2], columnlist1[3], columnlist1[4])       
        log.debug(sql)
        self.cursor.execute(sql)
        self.connection.commit()
        self.cursor.close()

    def AddDataById(self, columnlist2):

        self.cursor = self.connection.cursor()
        sql = "INSERT INTO Zeiten(FahrerNR, Zwischenzeit1, Zwischenzeit2, Endzeit)VALUES (%d, '%s', '%s', '%s')"%(columnlist2[0], columnlist2[1], columnlist2[2], columnlist2[3])       
        print sql
        self.cursor.execute(sql)
        self.connection.commit()
        self.cursor.close()
        
    def GetAllData(self, table):

        self.cursor = self.connection.cursor()
        sql = 'SELECT * FROM %s' % table
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        self.cursor.close()
        log.debug(data)
        return data

    def GetDataById(self, ID):

        self.cursor = self.connection.cursor()
        sql = "SELECT * FROM Zeiten WHERE FahrerNR='%s'" % ID
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

Database().GetAllData('Fahrer')
