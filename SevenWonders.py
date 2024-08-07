#!/usr/bin/env python
# coding: utf-8

from Card import Card
from Board import Board
from Player import Player
from AI import AI_Player
import pandas as pd
import random
class SevenWonders:
    def __init__(self, num_players=3,num_human=1,expansions=["base"], fast_setup=False):
        self.num_players=num_players
        self.num_human=num_human
        self.expansions=expansions
        self.rand_boards=True
        self.Players = {}
        self.decks = []
        self.fast_setup = fast_setup
        
    def setup(self):
        player_names = []
        rand_names = list(pd.read_csv("random_names.csv").loc[:,"First Name"])
        if self.num_human > 0:
            for human in range(0,self.num_human):
                if self.fast_setup:
                    player_names.append(random.choice(rand_names))
                else:
                    print(f"Enter name for player {human+1}:")
                    player_names.append(input())

        
        if self.fast_setup or self.num_human == 0:
            self.rand_boards = True
        else:
            confirm = False
            while not confirm:
                choice = input("Play with random boards? y/n ")
                if choice.lower() == "y" or choice.lower() == "yes" or choice == "0":
                    self.rand_boards = True
                    confirm = True
                elif choice.lower() == "n" or choice.lower() == "no" or choice == "1":
                    self.rand_boards = False
                    confirm = True
                else:
                    print("please answer with yes or no")
                    
        for ai in range(0,(self.num_players - self.num_human)):            
            name = "ai" + str(ai+1)
            player_names.append(name)

        self.set_decks(self.expansions)
        self.set_boards(player_names, self.expansions)
        
        print("List of Players:")
        for player in self.Players:
            self.Players[player].view()
            print()
        self.set_neighbors(player_names)
        title = open("title_card.txt","r")
        print(title.read())

    def set_decks(self, expansions="base"):
        card_list = pd.read_csv("card _list.csv")
        age1_list = card_list.loc[(card_list['age']==1) & (card_list['player_count'] <= self.num_players)]
        age2_list = card_list.loc[(card_list['age']==2) & (card_list['player_count'] <= self.num_players)]
        age3_list = card_list.loc[(card_list['age']==3) & (card_list['player_count'] <= self.num_players) & (card_list['color'] != "purple")]
        purple = card_list.loc[card_list['color'] == "purple"]
        age3_list = pd.concat([purple.sample(n=(self.num_players+2)),age3_list])
        age_lists = [age1_list,age2_list,age3_list]
        age1 = []
        age2 = []
        age3 = []
        self.decks = [age1, age2,age3]
        for age in range(0,3):
            for index,card in age_lists[age].iterrows():
                self.decks[age].append(Card(card["age"],card["name"],card["cost"],card["build"],card["product"],card["color"]))
        #if("Cities" in expansion):
        #    cities_cards = pd.read_csv("cities_card_list")
        #    (rest of code)
        return self.decks
        
    def set_boards(self, player_names, expansions="base"):
        board_list = pd.read_csv('board_list.csv', skip_blank_lines=False)
        board_frame = ""
        for human in range(0,self.num_human):
            name = player_names[human]
            if(self.rand_boards):
                board_frame = board_list.sample(replace=False)
                board_list.drop(board_frame.index, inplace=True)
            else:
                board_name = ""
                while board_name not in board_list["name"].values:
                    print(f"{name}, please select a board from the list below:")
                    print(board_list["name"].to_string(index=False))
                    board_name = input()
                    if board_name not in board_list["name"].values:
                        print(f"{board_name} isn't a board")
                board_frame = board_list.loc[(board_list["name"] == board_name)]
                board_list.drop(board_list[board_list["name"] == board_name].index, inplace=True)
            
            board = Board(board_frame["name"],board_frame["start"],board_frame["color"],board_frame["num_stages"],board_frame["costs"],board_frame["rewards"],board_frame["time"])
            self.Players[name] = Player(name, board)
        
        num_ai = self.num_players-self.num_human
        for ai in range(self.num_players-num_ai, self.num_players):
            board_frame = board_list.sample(replace=False)
            board_list.drop(board_frame.index, inplace=True)
            board = Board(board_frame["name"],board_frame["start"],board_frame["color"],board_frame["num_stages"],board_frame["costs"],board_frame["rewards"],board_frame["time"])
            name = player_names[ai]
            self.Players[name] = AI_Player(name, board)
    
    def set_neighbors(self, player_names):
        n_edges = 0
        for player in range(0,self.num_players - 1):
            name = player_names[player]
            left = ""
            right = ""
            left_set = False
            right_set = False
            
            while not left_set and n_edges < self.num_players:
                if isinstance(self.Players[name], AI_Player) or self.fast_setup:
                    left = player_names[player + 1]
                    left_set = True
                else:
                    print(f"{name} who is sitting on your left?")
                    left = input()
                    if left not in player_names:
                        print(f"{left} is not a player")
                    elif left == name:
                        print("You can't pick yourself")
                    elif self.Players[left].get_neighbor("right") and n_edges < self.num_players - 1:
                        print(f"inner cycle detected. choose another player")
                    elif self.Players[left].get_neighbor("right"):
                        print(f"{left} already has a neighbor to their right. choose another player")
                    else:
                        left_set = True
            
            if n_edges < self.num_players:
                self.Players[name].set_left(self.Players[left])
                self.Players[left].set_right(self.Players[name])
            n_edges += 1
            
            while not right_set and n_edges < self.num_players:
                
                if isinstance(self.Players[name], AI_Player) or self.fast_setup:
                    right = player_names[player - 1]
                    if player == 0:
                        right = player_names[len(player_names) - 1]
                    right_set = True
                else:
                    print(f"{name} who is sitting on your right?")
                    right = input()
                    if right not in player_names:
                        print(f"{right} is not a player")
                    elif right == name:
                        print("You can't pick yourself")
                    elif self.Players[right].get_neighbor("left") and n_edges < self.num_players:
                        print(f"inner cycle detected. choose another player")
                    elif self.Players[right].get_neighbor("left"):
                        print(f"{right} already has a neighbor to their right. choose another player")
                    else:
                        right_set = True
            if n_edges < self.num_players:
                self.Players[name].set_right(self.Players[right])
                self.Players[right].set_left(self.Players[name])
            n_edges += 1
    
    def resolve_conflicts(self, age):
        tokens = ["age 1","age 2", "age 3", "defeat"]
        winners = {}
        tie = {}
        for name in self.Players:
            player = self.Players[name]
            mp = player.get_resources(special=True)["military"]
            left = player.get_neighbor("left")
            right = player.get_neighbor("right")
            left_mp = left.get_resources(special=True)["military"]
            right_mp = right.get_resources(special=True)["military"]
            
            
            if mp > left_mp:
                winners[name] = {"left":left.get_name()}
                player.add_resources([tokens[age]], is_token=True)

            elif mp < left_mp:
                player.add_resources([tokens[3]], is_token=True) #adds defeat
            else:
                tie[name] = {"left":left.get_name()}
                    
            if mp > right_mp:
                if name in winners:
                    winners[name].update({"right":right.get_name()})
                else:
                    winners[name] = {"right":right.get_name()}
                player.add_resources([tokens[age]], is_token=True)
            elif mp < right_mp:
                player.add_resources([tokens[3]], is_token=True)
            else:
                if name in tie:
                    tie[name].update({"right":right.get_name()})
                else:
                    tie[name] = {"right":right.get_name()}
        
        for name in self.Players:
            if name in winners:
                if len(winners[name]) > 1:
                    print(f"{name} won their conflict against {winners[name]['left']} and {winners[name]['right']}!")
                else:
                    neighbor = list(winners[name].keys())[0]
                    win_name = winners[name][neighbor]
                    print(f"{name} won their conflict against {win_name}")
            if name in tie:
                if len(tie[name]) > 1:
                    print(f"In their conflict against {tie[name]['left']} and {tie[name]['right']}, {name} tied with both!")
                else:
                    neighbor = list(tie[name].keys())[0]
                    tie_name = tie[name][neighbor]
                    print(f"{name} was tied in their conflict against {tie_name}")
                    
    def add_science_vp(self, player):
        resources = player.get_resources(special=True)
        science = {symbol:resources[symbol] for symbol in ("cog", "compass", "tablet", "any_science") if symbol in resources}
        all = True
        max = {}
        if science["any_science"] > 0:
            has_zero = []
            for symbol in science:
                if science[symbol] == 0:
                    has_zero.append(symbol)
                    all = False
                max.update({symbol:(science[symbol] + science["any_science"])**2})
            
            max = sorted(max.items(), key = lambda x: x[1], reverse=True) #sorts max in asending order (symbol, value)
            if max[0][1] < 7 and len(has_zero) == 1:
                science[has_zero[0]] = 1
                all = True
            elif max[0][1] < 7 and len(has_zero) == 2 and science["any_science"] > 1:
                science[has_zero[0]] = 1
                science[has_zero[1]] = 1
                all = True
            else:
                science[max[0][0]] += science["any_science"]
        
        
        vp = 0
        for symbol in science:
            vp += science[symbol] ** 2
        if all:
            vp += 7
        
        victory = []
        for v in range(0,vp):
            victory.append("victory")
        
        player.add_resources(victory, is_card=False)
        return vp
    
    def add_military_vp(self, player):
        tokens = player.get_resources(special=True)["tokens"]
        token_values = {'age 1':1, "age 2":3, "age 3":5, "defeat":-1}
        vp = 0
        for token in tokens:
            for t in range(0,tokens[token]):
                vp += token_values[token]

        return vp
    def tally_victory(self):
        
        ranking = {}
        for name in self.Players:
            player = self.Players[name]
            print(name)
            military = self.add_military_vp(player)
            print(f"military: {military}")
            treasury = int(player.get_resources()["coin"]/3)
            print(f"treasury: {treasury}")
            #wonder = 0
            #structures = 0
            #commerce = 0 #yellow cards
            #guilds = 0
            science = self.add_science_vp(player)
            print(f"science: {science}")
            other = player.get_resources(special=True)["victory"]
            print(f"other: {other}")
            total = military + treasury + science + player.get_resources(special=True)["victory"]
            print(f"total: {total}")
            ranking[name] = total
        
        ranking = sorted(ranking.items(), key = lambda x: x[1], reverse=True)

        return ranking
        
    def play(self):
        if not self.Players:
            print("Please setup players first")
            return
        hand = {}
        discard_pile = {}
        num_cards = len(self.decks[0]) #all ages should have the same # of cards
        initial_hand_size = int(num_cards/self.num_players)
        
        for age in range(0,3):
            #sets initial hand for each age
            for n in self.Players:
                hand = {}
                cards = random.sample(self.decks[age],k=initial_hand_size)
                for card in cards:
                    self.decks[age].remove(card)
                    hand[card.get_name()] = card #formats hand for each card be searched by card name
                self.Players[n].set_hand(hand)
                
            turn = 0
            while turn < initial_hand_size - 1:
                action = 0
                card = ""
                old_hands = {}
                turn_actions = {}
                turn_cards = {}
                
                for name in self.Players:
                    player = self.Players[name]
                    action, card = player.set_action()
                    
                    if action == 2:
                        discard_pile.update({card:player.get_hand()[card]})
                    turn_actions[name] = action
                    turn_cards[name] = card
                    
                for name in self.Players:
                    player = self.Players[name]
                    old_hands[name] = player.play_card(turn_actions[name], turn_cards[name])
                    player.give_trade()

                    if turn == initial_hand_size - 2:
                        discarded = list(old_hands[name].keys())[0]
                        discard_pile.update({discarded:old_hands[name][discarded]})
                    
                    if (age == 0 or age == 2):
                        right = player.get_neighbor("right")
                        if right.get_name() in old_hands:
                            new_hand = old_hands[right.get_name()]
                        else:
                            new_hand = right.get_hand()
                    else:
                        left = player.get_neighbor("left")
                        if left.get_name() in old_hands:
                            new_hand = old_hands[left.get_name()]
                        else:
                            new_hand = left.get_hand()
                        
                    self.Players[name].set_hand(new_hand)
                    self.Players[name].set_discard(discard_pile)
                turn += 1
            self.resolve_conflicts(age)
        
        for n in self.Players:
            self.Players[n].activate_end_events()
            
        ranking = self.tally_victory()
        for i,rank in enumerate(ranking):
            if i == 0:
                print(f"1st place: {rank[0]} with {rank[1]} victory points")
            elif i == 1:
                print(f"2nd place: {rank[0]} with {rank[1]} victory points")
            elif i == 2:
                print(f"3rd place: {rank[0]} with {rank[1]} victory points")
            else:
                print(f"{i + 1}th place: {rank[0]} with {rank[1]} victory points")
            