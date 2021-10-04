from re import A
from typing import List, AnyStr
from itertools import product 
import random 
import time
import os


figures = ["Spades", "Clubs", "Hearts", "Diamonds"]
valuesShow = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
valuesAbsolute = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
statusDescription = ["Playing\t", "Black Jack!", "Win\t", "Lose\t", "Stand\t", "Push\t"]
stPlaying, stBlackJack, stWin, stLose, stStand, stPush = 0, 1, 2, 3, 4, 5
Playersnames = ["C. Darwin", "Aristóteles", "J. César", "Platón  ", "A. Einstein", "L. Pasteur", 
                "A. Mozart", "L. King", "Pitágoras", "N. Tesla", "M. Curie", "Arquímedes", "Socrates", "M. Angel"]
maxPlayers = len(Playersnames)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

class Card: 
    """ Class Card  """
    def __init__(self, figure: int, value: int): 
        self.figure = figure 
        self.value = value

    def getValue(self) -> int:
        return self.value 

    def __str__(self) -> AnyStr: 
        return f"{valuesShow[self.value]} of {figures[self.figure]}" 

    def __repr__(self) -> AnyStr: 
        return f"{valuesShow[self.value]} of {figures[self.figure]}"



class Player:
    """ Class Player. Uses class: Card  """
    def __init__(self, name: AnyStr, isdealer = False):
        self._name = name
        self._cards = []
        self.position = 0
        self._status = stPlaying
        self.isDealer = isdealer

    def setStatus(self, status: int) -> None:
        """ Set status player using list statusDescription """
        self._status = status

    def showCards(self) -> None:     
        """ Show list of cards""" 
        for idx in range(len(self._cards)):
            yield self._cards[idx]

    def addAce(self) -> None:
        """ Ace require validation, may take value of 1, 10 or 11 according to play"""
        if len(self._cards)==2:
            if valuesAbsolute[self._cards[0].value]==10:
                self.position = 21
                self.setStatus(stBlackJack)
            else:
                self.position += 10
        else: 
            if self.position <= 11:
                self.position += 10
            else:
                self.position += 1
    
    def getStatusDescription(self) -> AnyStr:
        return statusDescription[self._status]

    def addCard(self, card: Card) -> None:
        """ Add card to player"""
        if self._status == 0:
            self._cards.append(card)

            if card.getValue() == 0:
                self.addAce() # Ace require rule special for sum
            else:
                self.position += valuesAbsolute[card.getValue()]

            
            if len(self._cards) == 2 and self._cards[0].getValue() == 0 and valuesAbsolute[card.getValue()] == 10:
                self.position = 21


            if self.position > 21:
                self.checkAcePrevious()
                if self.position > 21:
                    self.setStatus(stLose)
            
            if self.position == 21:
                self.setStatus(stBlackJack)

            
            
            if not self.isDealer:
                print(f'{self._name} -> Card: {card} -> Position: {self.position} -> {statusDescription[self._status]}         ', end='\r')
        else:
            if not self.isDealer:
                print(f'End Game -> {self.getStatusDescription()} with {self.position} ')


    def checkAcePrevious(self) -> None:
        """ Recalcule posicion for Ace (10) to Ace (1) according to play """
        self.position = 0        
        for card in self._cards:
            self.position += valuesAbsolute[card.getValue()]

    def __str__(self) -> AnyStr: 
        return f"{self._name}" 

    def __repr__(self) -> AnyStr: 
        return f"{self._name}"

 
class Deck:
    """A class for a deck of cards; simulates a standard 4 suit deck. Uses class: Card""" 
    def __init__(self):
        self._deck = []
        self.startDeck()
        
    def startDeck(self) -> None:
        self._deck = self.getNewDeck()

    def getNewDeck(self) -> List[Card]:
        """ Populate the initial deck (4 figures * 13 values = 52 Cards)"""
        newDeck = [Card(s, f) for s, f in product(range(4), range(13))]  
        random.shuffle(newDeck)
        return newDeck

    def cardCount(self) -> int:
        """ Current cards count """
        return len(self._deck)
 

    def pickCard(self) -> Card: 
        """Pick a card from the pila of deck """ 
        if self.cardCount() > 0:
            return self._deck.pop()
 
    def shuffle(self) -> None: 
        """Shuffle the deck""" 
        random.shuffle(self._deck)
 
class BlackJack:
    """ Class Black Jack, uses classes: Deck, Player """
    def __init__(self, numPlayers: int):
        """Initialice playing with N players """
        namesPlayersRandom = Playersnames[:]
        self.players = []
        self.active = True
        self.topCards = True
        self.deckPlay = Deck()
        self.Dealer = Player('Dealer', True)

        random.shuffle(namesPlayersRandom)
        
        if numPlayers > maxPlayers:
            numPlayers = maxPlayers
            print(f'Max of players is {maxPlayers}')

        for _ in range(numPlayers):
            self.players.append(Player(namesPlayersRandom.pop()))

    def dealerInitial(self) -> None:
        """ Dealer initial for Balck Jack, two cards for player """
        clearConsole()
        print('-----------  Dealing...  -------------')
        
        for _ in range(2):
            for idx in range(len(self.players)):
                self.players[idx].addCard(self.deckPlay.pickCard())
                time.sleep(.07)
        
        self.Dealer.addCard(self.deckPlay.pickCard())
        self.Dealer.addCard(self.deckPlay.pickCard())

    def resetGame(self) -> None:
        self.deckPlay.startDeck()
        self.dealerInitial()

    def playDealer(self) -> None:
        """ Turn of the Dealer play. When not exist players playing thios methos is called """
        self.printSatus()
        while (len(self.getPlayersInStand()) > 0) or (len(self.getPlayersInPush()) > 0):  
            
            self.setUpdateStatusPlayers(self.Dealer.position)
            
            if (len(self.getPlayersInStand()) > 0) or (self.Dealer.position <= 21):
                time.sleep(.5)
                self.Dealer.addCard(self.deckPlay.pickCard())
                self.setUpdateStatusPlayers(self.Dealer.position)
                self.printSatus()
            

    def setUpdateStatusPlayers(self, dealerPosition: int) -> None:
        """ Thos methos is call when position Dealer is change """
        for player in list(filter( lambda player: player._status != stBlackJack and player.position < 21  , self.players )):
            time.sleep(.05)
            if dealerPosition > 21:
                player.setStatus(stWin)
            else:
                if dealerPosition > player.position:
                    player.setStatus(stLose)

                if dealerPosition == player.position:
                    player.setStatus(stPush)
            self.printSatus()

    #def showPLayers(self) -> List[Player]:
    #    players = []
    #    for idx in range(len(self.players)):
    #        players.append([self.players[idx]])
    #        yield players

    def printSatus(self, _player=None) -> None:
        clearConsole()
        print(f'\n¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯  {bcolors.BOLD}{bcolors.HEADER}Black Jack{bcolors.ENDC} {bcolors.WARNING}(demo made for Devisingh Balot ){bcolors.ENDC}  ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯')
       
        print(f'Cards in deck: {self.deckPlay.cardCount()}')
        if self.active:
            print(f'{bcolors.BOLD}Cards Dealer: {bcolors.UNDERLINE}{bcolors.OKBLUE}[(Hide), {list(self.Dealer.showCards())[0]}] {bcolors.ENDC}')
        else: 
            print(f'{bcolors.BOLD}Cards Dealer: {bcolors.UNDERLINE}{bcolors.OKGREEN}[Position: {self.Dealer.position}] {bcolors.OKBLUE}{list(self.Dealer.showCards())}{bcolors.ENDC}')
        
        if self.topCards:
            print(f'\nTop 10 cards of the deck: ', end='')
            print(self.showTopCards())
            print(f'Next card: {self.deckPlay._deck[-1] }')

        print(f'\n      Players\t\t|\tPosicion \t|\t State\t\t|\tCards')
        print('-------------------------------------------------------------------------------------------------------')
        
        for idx in range(len(self.players)):
            player = self.players[idx]
            if _player == player:
                print(f'{bcolors.OKGREEN}{idx+1}.\t{player._name } \t|\t  {player.position}\t\t|\t{player.getStatusDescription()}\t| {list(player.showCards())}{bcolors.ENDC}')
            else:
                print(f'{idx+1}.\t{player._name } \t|\t  {player.position}\t\t|\t{player.getStatusDescription()}\t| {list(player.showCards())}')
                
        self.showOptions()
    
    def showTopCards(self) -> List[Card]:
        topCards = [card for card in reversed(self.deckPlay._deck[-10:])]
        return topCards
    
    def getPlayersInGame(self) -> List[Player]:
        return list(filter( lambda player: player._status == stPlaying  , self.players ))

    def getPlayersInStand(self) -> List[Player]:
        return list(filter( lambda player: player._status == stStand  , self.players ))

    def getPlayersInPush(self) -> List[Player]:
        return list(filter( lambda player: player._status == stPush and player.position < 21  , self.players ))

    def setPushToWin(self, dealerPosition) -> None:
        for player in list(filter( lambda player: player._status == stPush  , self.players )):
            player.setStatus(stWin)

    def showOptions(self) -> None:
        print(f"\nOptions: {bcolors.OKCYAN}[0: Exit game] [1: Reset Game] [2: Shuffle current Deck] [3: Show top 10 cards of the deck] [4: Hide top 10 cards of the deck]{bcolors.ENDC}")

    def shuffleDeck(self) -> None:
        """ Requeriment Challenge """
        self.deckPlay.shuffle()

if __name__ == '__main__':
    clearConsole()
    print('Enter number of players (Max: 14)')
    print('> ', end='')
    numPlayers = int(input().rstrip())

    bj = BlackJack(numPlayers)
    bj.dealerInitial()
    exitGame = False
    clearConsole()

    while not exitGame:
        if bj.active:
            if len(bj.getPlayersInGame())>0:
                
                for player in bj.getPlayersInGame():
                    inputUser = ''

                    while inputUser not in ['h', 's', '0', '1', '2', '3', '4']:
                        bj.printSatus(player)
                        print(f'\n -> Turn:  {bcolors.OKGREEN}{player}  {bcolors.UNDERLINE}Position: {player.position}{bcolors.ENDC}\tChois: {bcolors.OKCYAN}[h: Hit] [s: Stand]{bcolors.ENDC} \r')
                        print('> ', end='')
                        inputUser = input().rstrip()

                    if inputUser=='0':
                        exitGame = True
                        break

                    if inputUser=='1':
                        bj = BlackJack(numPlayers)
                        bj.dealerInitial()
                        break

                    if inputUser=='2':
                        bj.shuffleDeck()
                        bj.printSatus(player)
                        break

                    if inputUser=='3':
                        if not bj.topCards:
                            bj.topCards = True
                            bj.printSatus(player)
                        break

                    if inputUser=='4':
                        if bj.topCards:
                            bj.topCards = False
                            bj.printSatus(player)
                        break

                    if inputUser=='h':
                        player.addCard(bj.deckPlay.pickCard())
                        
                    if inputUser=='s':
                        player.setStatus(stStand)
            else:    
                bj.active = False
                bj.playDealer()
                inputUser = ''

                while inputUser not in ['0', '1']:
                    print('----')
                    print('> ', end='')
                    inputUser = input().rstrip()

                exitGame = inputUser=='0'
    
                if inputUser=='1':
                    bj = BlackJack(numPlayers)
                    bj.dealerInitial()

    print(f'\n{bcolors.WARNING}    - Thanks for trying the demo, made for Devisingh Balot - {bcolors.ENDC} \n')            