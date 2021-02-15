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

    def __init__(self, create):
        if create:
            for i in range(6, 15):
                self.number = self.number + str(random.randint(0, 9))
            self.number = self.number + str(self.generateChecksumDigit())
            repeated = False
            for card in cardsDatabase:
                if card.number == self.number:
                    repeated = True
                    break
            while repeated:
                for i in range(6, 16):
                    self.number[i] = random.randint(0, 9)
                repeated = False
                for card in cardsDatabase:
                    if card.number == self.number:
                        repeated = True
                        break
            for i in range(0, 4):
                self.pin = self.pin + str(random.randint(0, 9))
            biggestID = 0
            for card in cardsDatabase:
                if card.id > biggestID:
                    biggestID = card.id
            self.id = biggestID
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
    # cur.execute("""INSERT INTO card (number, pin, balance)
    #                 VALUES ({0}, {1}, {2})
    #                 ;""".format(card.getCardNumber(), card.getCardPIN(), card.getCardBalance()))
    cur.execute(f"INSERT INTO card (number, pin, balance) VALUES ({card.getCardNumber()}, {card.getCardPIN()}, "
                f"{card.getCardBalance()});")
    conn.commit()
    startProgram()


def logIntoAccount():
    print("Enter your card number:")
    cardNumber = str(input())
    print("Enter your PIN:")
    pin = str(input())
    cur.execute(f"SELECT * FROM card WHERE number={cardNumber} AND pin={pin}")
    if bool(cur.fetchone()) is not False:
        print("You have successfully logged in!\n")
    else:
        print("Wrong card number or PIN!\n")
    selectedCard = Card(False)
    selectedCard.id = cur.fetchone()[0]
    selectedCard.number = cur.fetchone()[1]
    selectedCard.pin = cur.fetchone()[2]
    selectedCard.balance = cur.fetchone()[3]
    loggedMenu(selectedCard)


def loggedMenu(card):
    print("1. Balance")
    print("2. Log out")
    print("0. Exit")
    option = int(input())
    if option == 1:
        print(card.balance)
    elif option == 2:
        print("You have successfully logged out!\n")
        startProgram()
    else:
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
        print("Bye!\n")
        sys.exit()


# ACTUAL PROGRAM START
startProgram()
