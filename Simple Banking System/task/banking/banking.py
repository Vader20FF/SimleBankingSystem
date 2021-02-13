import random
import sys

cardsDatabase = []


class Card:
    number = "400000"
    pin = ""
    balance = 0

    def __init__(self):
        global cardsDatabase
        for i in range(6, 16):
            self.number = self.number + str(random.randint(0, 9))
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

    def getCardNumber(self):
        return self.number

    def getCardPIN(self):
        return self.pin

    def getCardBalance(self):
        return self.balance



def createAnAccount():
    global cardsDatabase
    card = Card()
    cardsDatabase.append(card)
    startProgram()


def logIntoAccount():
    global cardsDatabase
    print("Enter your card number:")
    cardNumber = str(input())
    print("Enter your PIN:")
    pin = str(input())
    selectedCard = None
    for card in cardsDatabase:
        if card.number == cardNumber:
            if card.pin == pin:
                selectedCard = card
                print("You have successfully logged in!\n")
            else:
                print("Wrong card number or PIN!\n")
        else:
            print("Wrong card number or PIN!\n")
    loggedMenu(selectedCard)


def loggedMenu(card):
    print("1. Balance")
    print("2. Log out")
    print("0. Exit")
    option = int(input())
    if option == 1:
        print(card.getCardBalance())
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
