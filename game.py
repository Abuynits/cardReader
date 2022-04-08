import random

class Player:
    def __init__(self, cards=[]):
        cards.sort()
        self.cards = cards  # list of own cards that can be played
        self.penalties = []  # list of cards as penalties - out of game

    def show_player(self):
        print("cards: ", end="")
        for c in self.cards:
            print(c, ",", end="")
        print()


def game_setup(number_players, player_array, cd):
    if 4 <= number_players <= 10:
        total_cards = number_players * 11
        allCards = []
        for card in range(1, total_cards):
            allCards.append(card)
        random.shuffle(cd)

        for i in range(number_players):
            p = Player()
            for j in range(10 * i, 10+10 * i):
                p.cards.append(allCards[0])
                allCards.pop(0)
            player_array.append(p)
        count = 0

        for c in allCards:
            cd[count][0] = c
            count += 1

    # at the end, the card deck = 4 starter cards, while the players have their own cards


def show_gameboard(card_deck):
    for r in range(len(card_deck)):
        for c in range(len(card_deck[0])):
            print(card_deck[r], [c], ",", end="")
        print()


# test:
player_arr = []
rows, cols = (4, 5)
card_deck = [[0]*cols]*rows

game_setup(5, player_arr, card_deck)

show_gameboard(card_deck)
for p in player_arr:
    p.show_player()

# TODO: need to assign point values to cards...
