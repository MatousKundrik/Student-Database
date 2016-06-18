register = dict()
username = ""
password = ""


def createfileheader():
    line = ""
    for i in range(0, len(headers)):
        line += headers[i].strip()
        if i != len(headers)-1:
            line += '\t'
    return line


def createfileline(student):
    line = ""
    for i in range(0, len(headers)):
        line += student[headers[i]]
        if i != len(headers)-1:
            line += '\t'
    return line


def createfile(student, register):
    filecontent = createfileheader() + "\n"

    for id in sorted(register.keys()):
        filecontent += createfileline(register[id]) + "\n"
    return filecontent


with open("Database.txt", "r") as datafile:
                lineCounter = 0
                for line in datafile:
                    lineCounter += 1
                    columns = line.split("\t")
                    if lineCounter == 1:
                        headers = columns
                    else:
                        student = dict()
                        for i in range(0, len(headers)):
                            student[headers[i]] = columns[i].strip()
                        register[student[headers[0]]] = student
                datafile.close()

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
            whattodo = input("What would you like to do? ListDetails / ChangeDetails: ").lower()
            if whattodo == "listdetails":
                student = register[input("Please enter the student id of the requested student: ")]
                print(headers)
                print(createfileline(student))
            elif whattodo == "changedetails":
                student = register[input("Which students details would you like to change?: ")]
                print(headers)
                print(createfileline(student))
                whichcategory = input("Which piece of data would you like to change?: ")
                print(student[whichcategory])
                datachange = input("What would you like to change this to?: ")
                del student[whichcategory]
                student[whichcategory] = datachange
                print(createfileline(student))
                with open("Database.txt", "w") as writefile:
                    writefile.write(createfile(student, register))
            else:
                print("This is not a valid operation")
                continue
