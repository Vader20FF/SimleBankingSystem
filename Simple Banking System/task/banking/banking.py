import random
import sys
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

class Card:
    id = ...
    number = "400000"
    pin = ""
    balance = 0

    def __init__(self, existing):
        if existing:
            for i in range(6, 15):
                self.number = self.number + str(random.randint(0, 9))
            self.number = self.number + str(self.generateChecksumDigit())
            repeated = False
            cur.execute(f"SELECT * FROM card WHERE number={self.number}")
            if bool(cur.fetchone()) is True:
                repeated = True
            while repeated:
                for i in range(6, 16):
                    self.number[i] = random.randint(0, 9)
                repeated = False
                cur.execute(f"SELECT * FROM card WHERE number={self.number}")
                if bool(cur.fetchone()) is True:
                    repeated = True
            for i in range(0, 4):
                self.pin = self.pin + str(random.randint(0, 9))
            biggestID = 0
            print("Your card has been created\n")
            print("Your card number:")
            print(self.getCardNumber())
            print("Your card PIN:")
            print(self.getCardPIN())

    def getCardInfo(self):
        print("Your card number:")
        print(self.getCardNumber())
        print("Your card PIN:")
        print(self.getCardPIN())
        print("Your card balance:")
        print(self.getCardBalance())

    def getCardID(self):
        return self.id

    def getCardNumber(self):
        return self.number

    def getCardPIN(self):
        return self.pin

    def getCardBalance(self):
        return self.balance
    
    def setCardID(self, newID):
        self.id = newID
        
    def setCardNumber(self, newCardNumber):
        self.id = newCardNumber
        
    def setCardPIN(self, newCardPIN):
        self.id = newCardPIN
        
    def setCardBalance(self, newCardBalance):
        self.id = newCardBalance

    def generateChecksumDigit(self):
        # originalNumber
        # drop the last digit
        tempListNumber = list(self.number)
        # multiply odd digits by 2
        for i in range(0, 15, 2):
            digitToMultiply = int(tempListNumber[i])
            tempListNumber[i] = str(digitToMultiply * 2)
        # subtract 9 to numbers over 9
        for index, digit in enumerate(tempListNumber):
            if int(digit) > 9:
                tempListNumber[index] = int(digit) - 9
        # add all numbers
        numbersSum = 0
        for digit in tempListNumber:
            numbersSum += int(digit)
        checksumDigit = 0
        if numbersSum % 10 == 0:
            return checksumDigit
        else:
            temp = 10
            while temp < numbersSum:
                temp += 10
            checksumDigit = temp - numbersSum
            return checksumDigit


def createAnAccount():
    card = Card(True)
    cur.execute(f"INSERT INTO card (number, pin, balance) VALUES ({card.getCardNumber()}, {card.getCardPIN()}, "
                f"{card.getCardBalance()});")
    conn.commit()
    startProgram()


def logIntoAccount():
    print("Enter your card number:")
    cardNumber = str(input())
    print("Enter your PIN:")
    pin = str(input())
    selectedCard = Card(False)
    for row in cur.execute(f"SELECT * FROM card WHERE number={cardNumber} AND pin={pin}"):
        selectedCard.setCardID(row[0])
        selectedCard.setCardNumber(row[1])
        selectedCard.setCardPIN(row[2])
        selectedCard.setCardBalance(row[3])
    cur.execute(f"SELECT * FROM card WHERE number={cardNumber} AND pin={pin}")
    if bool(cur.fetchone()) is not False:
        print("You have successfully logged in!\n")
        loggedMenu(selectedCard)
    else:
        print("Wrong card number or PIN!\n")
        startProgram()


def loggedMenu(card):
    while True:
        print("\n1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")
        option = int(input())
        if option == 1:
            checkBalance(card)
        elif option == 2:
            addIncome(card)
        elif option == 3:
            doTransfer(card)
        elif option == 4:
            closeAccount(card)
        elif option == 5:
            logOut()
        else:
            exit()


def checkBalance(card):
    print(card.balance)


def addIncome(card):
    print("Enter income:")
    income = int(input())
    card.balance += income
    cur.execute(f"UPDATE card SET balance={card.balance} WHERE number={card.getCardNumber()}")
    conn.commit()
    print("Income was added!")


def doTransfer(card):
    print("Enter card number:")
    receiverCardNumber = input()
    tempCard = Card(False)
    tempCard.setCardNumber(receiverCardNumber[:-1])
    if card.getCardNumber() == receiverCardNumber:
        print("You can't transfer money to the same account!\n")
    elif tempCard.generateChecksumDigit() != int(receiverCardNumber[-1]):
        print("Probably you made a mistake in the card number. Please try again!\n")
    else:
        cur.execute(f"SELECT * FROM card WHERE number={receiverCardNumber}")
        if bool(cur.fetchone()) is not False:
            print("Enter how much money you want to transfer:")
            moneyToTransfer = input()
            cur.execute(f"SELECT balance FROM card WHERE number={card.getCardNumber()}")
            if cur.fetchone() < moneyToTransfer:
                "Not enough money!\n"
            else:
                cur.execute(f"UPDATE card SET balance = {card.balance} - {moneyToTransfer} "
                            f"WHERE number={card.getCardNumber()}")
                conn.commit()
                cur.execute(f"UPDATE card SET balance = {card.balance} + {moneyToTransfer} "
                            f"WHERE number={receiverCardNumber}")
                conn.commit()
                "Success"
        else:
            print("Such a card does not exist.\n")


def closeAccount(card):
    cur.execute(f"DELETE FROM card "
                f"WHERE number={card.getCardNumber()}")
    conn.commit()
    print("The account has been closed!\n")


def logOut():
    print("You have successfully logged out!\n")
    startProgram()


def exit():
    print("Bye!\n")
    sys.exit()


def startProgram():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    option = int(input())
    if option == 1:
        createAnAccount()
    elif option == 2:
        logIntoAccount()
    else:
        exit()


# ACTUAL PROGRAM START
startProgram()
