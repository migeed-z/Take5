from random import randrange, shuffle, random, seed
from copy import deepcopy
from retic import List, Void, Tuple, Bool
from player import Player

min_val = 2
max_val = 7
turns = 10
stack_size = 5
deck_size = 210

class Dealer:
    """
    To represent the Dealer for the whole game
    """

    def __init__(self:Dealer, players:List(Player), bull_points:List(int))->Void:
        """
        :param deck: [Card ...]
        :param players: [Player ...]
        :param bull_points: [Int ...]
        """
        self.deck = self.create_deck()
        self.players = players
        self.bull_points = bull_points

    def simulate_game(self:Dealer)->List(Tuple(int, int)):
        """
        Similulates a game and returns the players' scores
        :return: [Tuple ...]
        """
        while not self.is_over():
            self.simulate_round()
        return self.output_scores()

    def simulate_round(self:Dealer)->Void:
        """
        Simulates a complete round of 10 turns
        :return: None
        """
        self.hand()
        stacks = self.create_stacks()
        for i in range(turns):
            for j in range(len(self.players)):
                player = self.players[j]
                chosen_stack_index = player.choose_correct_stack(stacks)
                (p, s) = self.update_game(player, chosen_stack_index, stacks)
                self.bull_points[j]+=p
                stacks = s

    #Problem: if you change return type to Tuple(int), it will pass guarded check and not pass transient.
    def create_deck(self:Dealer, deck_size:int = deck_size, bull_points:float = .5, order:float = .5)->List(Tuple(int, int)):
        """
        :param deck_size: Int, number of cards in deck
        :param min: Int, minimum number of bull points
        :param max: Int, maximum number of bull points
        :param bull_points: float, bull points parametrization
        :param order: float, order of cards parametrization
        :return: [Card ...]
        """
        seed(bull_points)
        cards = []
        for i in range(deck_size):
            cards.append((i+1, randrange(min_val, max_val)))
        s = (order or random())
        shuffle(cards, lambda: s)
        return cards

    def hand(self:Dealer)->Void:
        """
        Hand cards to players and update deck and players' cards
        accordingly
        :return: None
        """
        for i, player in enumerate(self.players):
            #hand = self.deck[:i+1*10]
            hand = []
            for i in range(i+1 * 10, i + 2 * 10):
                hand.append(self.deck[i])
            player.take_hand(hand)

    def create_stacks(self:Dealer)->(List(List(Tuple(int, int)))):
        """
        create 4 new stacks each having 1 card from the deck
        at the start of every round
        Initialize all players with that stack
        :return: [[Tuple] ...]
        """
        stacks = []
        for i in range(4):
            stacks.append([self.deck.pop()])
        return stacks

    def is_over(self:Dealer)->Bool:
        """
        Is the game over?
        :return: Boolean
        """
        return max(self.bull_points) >= 66

    def output_scores(self:Dealer)->List(Tuple(int, int)):
        """
        Outputs the names of the winning and losing players
        :param players: [Player ...]
        :return: (Player, Player)
        """
        res = []
        for i in range(len(self.players)):
            player_points = self.bull_points[i]
            player_name = self.players[i].name
            res.append((player_name, player_points))
        return res

    def update_game(self:Dealer, player:Player, stack_index:int, stacks:List(List(Tuple(int, int))))->\
            Tuple(int, List(List(Tuple(int, int)))):
        """
        update playe's bull points based on chosen stack
        :param stack_index: Int
        :param stacks: [[Tuple...]...] where len(stacks)=4
        :return: Tuple
        """
        top_cards = list(map(lambda stack: stack[-1], stacks))
        discarded_index = player.discard()
        discarded = player.cards.pop(discarded_index)

        if discarded[0] < min(list(map(lambda card: card[0], top_cards))):
            bull_points = self.get_sum(stacks[stack_index])

            new_stacks = self.replace_card(discarded, stack_index, stacks)
            return bull_points, new_stacks

        else:
            my_stack = stacks[stack_index]
            if len(my_stack) == stack_size:
                bull_points = self.get_sum(my_stack)
                new_stacks = self.replace_card(discarded, stack_index, stacks)
                return (bull_points, new_stacks)
            else:
                new_stacks = self.add_card(discarded, stack_index, stacks)
                return 0, new_stacks

    def get_sum(self:Dealer, stack:List(Tuple(int, int)))->int:
        """
        returns the player's bull points per turn
        :param stack: [Tuples ...]
        :return Int
        """
        bull_points = sum(list(map(lambda card: card[1], stack)))
        return bull_points

    def replace_card(self:Dealer, card:Tuple(int, int), index:int, stacks:List(List(Tuple(int, int))))->List(List(Tuple(int, int))):
        """
        Replaces stack with card and returns new stack
        :param card: Tuple
        :param index: Int
        :param stacks: [[Tuples ...] ...]
        :return [[Tuple...]...]
        """
        new_stacks = deepcopy(stacks)
        new_stacks[index] = [card]
        return new_stacks

    def sum_stacks(self:Dealer, stacks:List(List(Tuple(int, int))))->List(int):
        """
        Sums the bull points of stacks
        :param stacks [[Tuple ...] ...] where len(stacks)=4
        :return: [Int, ...]
        """
        sums = []
        for stack in stacks:
            bull_points = list(map(lambda card: card[1], stack))
            sums.append(sum(bull_points))
        return sums

    def add_card(self:Dealer, card:Tuple(int, int), index:int, stacks:List(List(Tuple(int, int))))->List(List(Tuple(int, int))):
        """
        adds card on top of the stack[index]
        :param card: Tuple
        :param stack: [Tuple...]
        :return: [Tuple...]
        """
        new_stacks = deepcopy(stacks)
        new_stacks[index].append(card)
        return new_stacks
