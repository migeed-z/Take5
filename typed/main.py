from retic import Void,List,Int
from benchmark_tools.Timer import Timer
from player import Player
from dealer import Dealer
from benchmark_tools.Counter import counted, get_num_calls
from inspect import getmembers, isfunction


@counted
def generate_dealer(players:List(Player), cards_per_game:Int)->Dealer:
    """
    Instantiates the dealer which will take over the game
    :return: Dealer
    """
    points = [0 for i in range(len(players))]
    return Dealer(players, points, cards_per_game)

@counted
def generate_players(num_players:Int)->List(Player):
    """
    instantiates n players with an empty list of cards
    :param num_players: int
    :return: [Players...]
    """
    players = []
    for i in range(num_players):
        players.append(Player(i, []))
    return players

@counted
def main()->Void:

    num = 3 #number of players
    cards_per_player = 10
    cards_per_game = 210

    if num < 2:
        print('Too few players!')

    if cards_per_game/cards_per_player < num:
        print("Too many players!")
        exit()

    players = generate_players(num)
    dealer = generate_dealer(players, cards_per_game)
    dealer.simulate_game()

t = Timer()
with t:
  for i in range(500):
    main()


