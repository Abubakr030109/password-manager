import string
import random

userInput = str()
passwordList = {}
isFirstLoop = True

################################################################################


def shuffleChars(string: str) -> str:
    l = []
    for x in string:
        l.append(x)

    random.shuffle(l)
    string = ""

    for x in l:
        string += x

    return string


def loadPasswords():
    with open("My_Passwords.txt") as myFile:
        while True:
            line = myFile.readline()
            if line == '':
                break
            line = simpleEncryption(line)
            delimeter = line.index('|')
            service = line[:delimeter]
            passwordList[service] = line[delimeter+1:-1]


def simpleEncryption(text: str) -> str:
    newText = str()
    for i in range(len(text)):
        newDecimal = ord(text[i]) ^ 10
        # using the number 10 above, only 1 char is problematic. The character 'u'
        # so the character 'u' won't be incrypted
        if newDecimal >= 32 and newDecimal <= 126:
            newText += chr(newDecimal)
        else:
            newText += text[i]
    return newText


def findPassword():
    while True:
        print("\nWhich service would you like to see the password of? (case-sensitive)")
        print("Enter 'all' to see all passwords\n")
        userInput = input()
        print()
        if userInput == "all":
            for x in passwordList:
                print(x+": "+passwordList[x])
            break
        elif userInput in passwordList:
            print(userInput + ": " + passwordList[userInput])
            break
        else:
            print("Password doesn't exist for this service")
            userInput = input("Try again? (Y/N): ")
            if userInput.upper() != "Y":
                break


def generatePassword():
    userInput = input(
        "\nWhich service do you want to create a password for? ")
    newService = userInput

    if newService in passwordList:
        print("\nPassword already exists")
        return

    userInput = input("Defualt Mode or Advanced Mode? (D/A): ")

    if userInput.upper() == "D":
        passwordLength = 15
        nrUpperCaseChars = 3
        nrDigits = 3
        nrSpecialChars = 3
    else:
        while True:
            print("\nPassword Requirements")
            passwordLength = int(
                input("What should the length of your password be: "))
            nrUpperCaseChars = int(
                input("Minimum nr of uppercase characters: "))
            nrDigits = int(input("Minimum nr of digits: "))
            nrSpecialChars = int(input("Minimum nr of special characters: "))

            if (passwordLength < (nrUpperCaseChars + nrDigits + nrSpecialChars)):
                print(
                    "The chosen length of your password is too short for your other password requirements. Try again.")
            else:
                break

    upperCaseChars = str()
    digits = str()
    specialChars = str()

    for _ in range(nrUpperCaseChars):
        upperCaseChars += random.choice(string.ascii_uppercase)

    for _ in range(nrDigits):
        digits += random.choice(string.digits)

    for _ in range(nrSpecialChars):
        specialChars += random.choice(string.punctuation)

    nrRemainingChars = passwordLength - nrUpperCaseChars - nrDigits - nrSpecialChars
    allChars = string.ascii_letters + string.digits + string.punctuation
    remainingChars = str()
    for _ in range(nrRemainingChars):
        remainingChars += random.choice(allChars)

    newPassword = upperCaseChars + digits + specialChars

    newPassword = shuffleChars(newPassword) + remainingChars

    passwordList[newService] = newPassword

    print("\n" + newService + ": " + passwordList[newService])

    line = simpleEncryption(newService+"|"+passwordList[newService])

    with open("My_Passwords.txt", "a") as myFile:
        myFile.write(line+"\n")

    print("\nWrote to textfile")


def deletePassword():
    userInput = input("\nWhich password would you like to delete? ")
    passToDelete = userInput
    userInput = input("Are you sure? (Y/N): ")

    if userInput.upper() != "Y":
        return

    passExists = False
    with open("My_Passwords.txt", "w") as myFile:
        for x in passwordList:
            if passToDelete != x:
                line = simpleEncryption(x+"|"+passwordList[x])
                myFile.write(line+"\n")
            else:
                passExists = True

    if passExists:
        del passwordList[passToDelete]
        print("\nPassword Deleted")
    else:
        print("\nPassword doesn't exist for this service")

################################################################################


with open("Master_Password.txt") as myFile:
    line = simpleEncryption(myFile.readline())
    masterPass = line

userInput = input("Enter the master password: ")
while userInput != masterPass:
    print("\nWrong!")
    print("1: Try again")
    print("2: Create new Master Password\n")

    userInput = input()

    if userInput == "1":
        userInput = input("\nEnter the master password: ")
    elif userInput == "2":
        userInput = input("\nEnter old Master Password: ")

        while userInput != masterPass:
            userInput = input("Master Password Incorrect. Try again: ")

        userInput = input("Enter new Master Password: ")
        masterPass = userInput

        with open("Master_Password.txt", "w") as myFile:
            myFile.write(simpleEncryption(masterPass))

        print("\nNew Master Password created!")

loadPasswords()

while True:
    if (isFirstLoop):
        print("\nWhat would you like to do?")
    else:
        print("\nWhat else would you like to do?")

    print("1: Find Password")
    print("2: Generate Password")
    print("3: Delete Password")
    print("q: Quit\n")

    userInput = input()

    if userInput == "1":
        findPassword()
    elif userInput == "2":
        generatePassword()
    elif userInput == "3":
        deletePassword()
    else:
        break

    isFirstLoop = False
