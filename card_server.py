import random
import copy

class CardServer:
    def __init__(self, cardList, initialCount) -> None:
        self.cardList = cardList
        self.initialCount = initialCount
    
    def resetCards(self):
        print('Reset cards')
        self.cards = []
        for card in self.cardList:
            for _ in range(8):
                self.cards.append(copy.copy(card))

        random.shuffle(self.cards)

    def getNext(self, number):
        result = []
        while self.cards and number > 0:
            result.append(self.cards.pop(0))
            number -= 1
        
        if (number > 0):
            self.resetCards()
            result = result + self.getNext(number)

        return result
    
    def getInitial(self):
        self.resetCards()
        result = []
        randomList = self.cardList.copy()
        random.shuffle(randomList)
        if self.initialCount == 4:
            for _ in range(2):
                result.extend(copy.copy(card) for card in randomList)
        elif self.initialCount == 5 or self.initialCount == 7:
            result.extend(copy.copy(card) for card in randomList)
            result.append(copy.copy(randomList[0]))
        elif self.initialCount == 6:
            result.extend(copy.copy(card) for card in randomList)
        return result
    
    def addNext(self, card):
        self.cards.insert(0, card)

# server = CardServer(['A1', 'A2', 'B1', 'B2', 'C1', 'C2'], 7)
# print(server.getInitial())
# print(server.getNext(3))
# print(server.getNext(5))
# server.addNext('AU')
# print(server.getNext(7))
# print(server.getNext(7))
# print(server.getNext(7))
# print(server.getNext(7))
# print(server.getNext(7))
# print(server.getNext(7))
# print(server.getNext(7))
# print(server.getNext(7))
