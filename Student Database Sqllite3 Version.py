import sqlite3

conn = sqlite3.connect("sqlite3test.db")
c = conn.cursor()

def createtable():
    c.execute("CREATE TABLE IF NOT EXISTS studentdatatable(PupilID TEXT, FName TEXT, SName TEXT, BirthDate TEXT,"
              "HouseAddress TEXT, PhoneNumber TEXT, Gender TEXT, Form TEXT, Email TEXT)")


def databaseisempty():
    c.execute("SELECT COUNT(*) from studentdatatable")
    result = c.fetchone()
    number_of_rows = result[0]
    if number_of_rows == 0:
        return True
    else:
        return False


def loaddatafromfile(filename):
    with open(filename, "r") as datafile:
        lineCounter = 0
        for line in datafile:
            lineCounter += 1
            columns = line.split("\t")
            if lineCounter != 1:
                dataline=""
                for i in range(0, len(columns)):
                    dataline += "'" + columns[i] + "'"
                    if i != len(columns)-1:
                        dataline += ","
                c.execute("INSERT INTO studentdatatable VALUES({})".format(dataline))
                conn.commit()
        datafile.close()

createtable()
if databaseisempty():
    loaddatafromfile("Database.txt")

c.close()
conn.close()
