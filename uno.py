from dataclasses import dataclass
from enum import Enum


class Suit(Enum):
    RED = "Red"
    YELLOW = "Yellow"
    GREEN = "Green"
    BLUE = "Blue"
    WILD = "Wild"


class Action(Enum):
    DRAW_TWO = "Draw Two"
    DRAW_FOUR = "Draw Four"
    SKIP = "Skip"
    REVERSE = "Reverse"


@dataclass
class Card:
    suit: Suit
    number: int | Action


@dataclass
class Player:
    name: str
    hand: list[Card]


@dataclass
class State:
    discard_pile: list[Card]
    draw_pile: list[Card]
    player_order: list[Player]

    def __init__(self, players: str):
        raise NotImplementedError()

    def play_card(self, index: int):
        # assuming that input is already validated
        # index exists, card matches discard top
        card = self.player_order[0].hand.pop(index)
        self.discard_pile.append(card)
        # handle actions
        match card:
            case Card(action=Action.DRAW_TWO):
                ...
            case Card(action=Action.DRAW_TWO):
                ...
        self.player_order = self.player_order[1:] + [self.player_order[0]]

    def play_wild_card(self, index: int, suit: Suit):
        card = self.player_order[0].hand[index]
        card.suit = suit
        self.play_card(index)

    def draw_card(self):
        # assuming that draw pile is non-empty
        card = self.draw_pile.pop(0)
        self.player_order[0].hand.append(card)
