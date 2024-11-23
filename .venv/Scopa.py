import random
import pyinputplus as pyip
import time
import io

SEEDS = ["denars", "batons", "swords", "cups"]
VALUES =[i for i in range(1,11)]

class Card:
    def __init__(self,value, seed):
        self.value = value
        self.seed = seed

    def __repr__(self):
        return f"{self.value} of {self.seed}"


class Player:
    def __init__(self,name):
        self.name = name
        self.hand = []
        self.pile = []
        self.scope = 0



class Scopa:
    def __init__(self):
        self.nPlayers = 0
        self.deck = [Card(value, seed)for value in VALUES for seed in SEEDS]
        random.shuffle(self.deck)
        self.table = []
        self.players = [Player("human")]
        self.lastTake = 0


    def start_game(self, nPlayers):
        if (nPlayers not in range(1, 5)): raise ValueError(f"ERROR unable to start game with {nPlayers} players")
        self.players += [Player("AI" + str(n)) for n in range(1, nPlayers)]
        self.give_cards(nPlayers)
        self.show_table()
        self.turn_human()

    def give_cards(self, nPlayers):

        if not self.deck:  # Check if the deck is empty
            self.end_game()
            return
        else:
            for player in self.players:
                for _ in range(3):
                    if self.deck:  # Ensure there are cards to give
                        player.hand.append(self.deck.pop())
            for _ in range(4):
                if self.deck:  # Ensure there are cards to put on the table
                    self.table.append(self.deck.pop())

    def turn_human(self):
        chosen_card = "hey"
        if len(self.players[0].hand) == 0: self.give_cards(self.nPlayers);
        if len(self.players[0].hand) > 1:
            choice = pyip.inputMenu([str(card) for card in self.players[0].hand], numbered=True)
            chosen_card = next(card for card in self.players[0].hand if str(card) == choice)
        elif len(self.players[0].hand) == 1:
            input("Play the following card: " + str(self.players[0].hand[0]))
            chosen_card = self.players[0].hand[0]
        if chosen_card != "hey":
            self.players[0].hand.remove(chosen_card)
            removeCards = self.takeCard(chosen_card, self.table)
            self.table.append(chosen_card)
            if not removeCards:
                self.show_table()
            else:
                for card in removeCards:
                    self.players[0].pile.append(card)
                    self.table.remove(card)
                if not self.table:
                    self.players[i].scope += 1
                    print("SCOPA!")
                self.lastTake = 0
                self.show_table()
            self.ai_turn()


    def ai_turn(self):
        for i in range(1, len(self.players)):
            if len(self.players[i].hand) == 0:
                break
            chosen_card = self.bestMove(self.players[i], self.table)
            self.players[i].hand.remove(chosen_card)
            removeCards = self.takeCard(chosen_card, self.table)
            self.table.append(chosen_card)
            if not removeCards:
                self.show_table()
            else:
                for card in removeCards:
                    self.players[i].pile.append(card)
                    self.table.remove(card)
                if not self.table:
                    self.players[i].scope += 1
                    print("SCOPA AI!")
                self.lastTake = i
                self.show_table()
        self.turn_human()

    def end_game(self):
        for card in self.table:
            self.players[self.lastTake].pile.append(card)
        for player in self.players:
            print(player.name + " has " + str(player.scope) + " scope")
            for card in player.pile:
                if card.value == 7 and card.seed == "denars":
                    print(player.name + "has sette bello")

        cartelungo = max(self.players, key=lambda player: len(player.pile))
        print(cartelungo.name + " has the most cards: " + str(len(cartelungo.pile)) + " cards")

        carteOro = max(self.players, key=lambda player: len([card for card in player.pile if card.seed == "denars"]))
        print(carteOro.name + " has the most golden cards: " + str(len([card for card in carteOro.pile if card.seed == "denars"])) + " golden cards")

        settanta = max(self.players, key=lambda player: len([card for card in player.pile if card.value == 7]))
        print(settanta.name + " has the most 7s " + str(len([card for card in settanta.pile if card.value == 7])) + " 7s" )


    def show_table(self):
        for player in self.players:
            print(f"{player.name} has ", end = " ")
            for card in player.hand:
                print(card, end = ", ")
            print()
        print("Cards on table: ", end = " ")
        for card in self.table:
            print(card, end = ", ")
        print()

    def get_game_state(self):
        output = io.StringIO()  # Create a StringIO object to capture output

        # Capture player hands
        for player in self.players:
            output.write(f"{player.name} has ")
            output.write(", ".join(str(card) for card in player.hand))  # Join card names with commas
            output.write("\n")  # New line after each player's cards

        # Capture cards on the table
        output.write("Cards on table: ")
        output.write(", ".join(str(card) for card in self.table))  # Join table cards with commas
        output.write("\n")  # New line at the end

        return output.getvalue()

    @staticmethod
    def takeCard(chosen_card: Card, table: list[Card]) -> list[Card]:
        checkedCards = []
        possibleCards = []
        for card in table:
            if card.value == chosen_card.value:
                return [card, chosen_card]
            elif card.value < chosen_card.value:
                for card2 in checkedCards:
                    if chosen_card.value == (card.value + card2.value):
                        possibleCards = [card, card2, chosen_card]
            checkedCards.append(card)

        return possibleCards

    @staticmethod
    def bestMove(player: Player, table: list[Card]) -> Card:
        moves = []
        for card in player.hand:
            score = 0
            cardTaken = Scopa.takeCard(card, table)
            if cardTaken:
                for taken in cardTaken:
                    score += 0.5
                    if (taken.seed == "denars"):
                        score += 1
                    if (taken.value == 7):
                        score += 1.5
                    if (len(table) - len(cardTaken) == 1):
                        score -= 3
                    if (len(table) - len(cardTaken) == 0):
                        score += 5
            else:
                if card.value == "denars":
                    score -= 1
                if card.value == 7:
                    score -= 2
            moves.append((card, score))
            #print(f"the score is {score}! ")

        bestcard = max(moves, key=lambda move: move[1])[0]
        return bestcard



gioco = Scopa()
gioco.start_game(2)