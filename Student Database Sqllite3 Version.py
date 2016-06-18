import sys
import sqlite3
import texttable as tt

conn = sqlite3.connect("StudentDatabase.db")
c = conn.cursor()
username = ""
password = ""


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
        linecounter = 0
        for line in datafile:
            linecounter += 1
            columns = line.split("\t")
            if linecounter != 1:
                dataline = ""
                for i in range(0, len(columns)):
                    dataline += "'" + columns[i].strip() + "'"
                    if i != len(columns)-1:
                        dataline += ","
                c.execute("INSERT INTO studentdatatable VALUES({})".format(dataline))
                conn.commit()
        datafile.close()

createtable()
if databaseisempty():
    loaddatafromfile("Database.txt")


def printprettytable(rows):
    table = tt.Texttable(0)
    table.set_cols_dtype(["t", "t", "t", "t", "t", "t", "t", "t", "t"])
    table.add_row(
        ["PupilID", "FName", "SName", "BirthDate", "HouseAddress", "PhoneNumber", "Gender", "Form",
         "Email"])
    table.add_rows(rows, header=False)
    print(table.draw())
    return table


def getstudentdata():
    c.execute("SELECT * FROM studentdatatable WHERE PupilID=?", [student])
    return c.fetchone()


while True:
    print("Please login before using the student database")
    attemptusername = input("Please enter your username: ")
    attemptpassword = input("Please enter your password:")
    if username != attemptusername:
        print("Incorrect Username")
        continue
    elif password != attemptpassword:
        print("Incorrect Username")
        continue
    else:
        while True:
            whattodo = input("What would you like to? (ListDetails/ChangeDetails/Exit): ").lower()
            if whattodo == "listdetails":
                student = input("Enter the ID of the student you wish to see: ")
                printprettytable([getstudentdata()])
            elif whattodo == "changedetails":
                student = input("Which students details would you like to change?: ")
                printprettytable([getstudentdata()])
                whichcategory = input("Which piece of data would you like to change?: ")
                c.execute("SELECT {} FROM studentdatatable WHERE PupilID=?".format(whichcategory), [student])
                original = c.fetchone()[0]
                datachange = input("What would you like to change {} to?: ".format(original))
                c.execute("UPDATE studentdatatable SET {} = ? WHERE PupilID = ?".format(whichcategory),
                          [datachange, student])
                confirmcommit = input("Are you sure you want to update {} from {} to {}? (Y/N):"
                                      .format(whichcategory, original, datachange)).lower()
                if confirmcommit == "y":
                    conn.commit()
                    printprettytable([getstudentdata()])

                else:
                    conn.rollback()

            elif whattodo == "exit":
                c.close()
                conn.close()
                sys.exit()

            else:
                print("That is not a valid operation")
