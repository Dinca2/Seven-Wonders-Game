import Player
import random
import copy

class AI_Player(Player.Player):
    def __init__(self, name, board):
        super().__init__(name, board)
    
    def set_action(self):
        card_name = ""
        action = 0

        if not self.available_cards:
            self.available(self.hand)
    
        
        if self.stage["available"]:
            card_name = random.choice(list(self.hand))
            action = 3
        elif self.available_cards:
            card_name = random.choice(list(self.available_cards))
            action = 1 #play
        elif self.trade_cards:
            card_name = random.choice(list(self.trade_cards))
            action = 1 #trade
            self.confirm_trade(card_name)
        else:
            card_name = random.choice(list(self.unavailable))
            action = 2
        
        return action, card_name
    
    def confirm_trade(self, card_name):
        needed_resources = {"wood":0,"stone":0,"brick":0,"ore":0,"glass":0,"silk":0,"paper":0}
        right_coins = 0
        left_coins = 0
        self.left_coins = 0
        self.right_coins = 0
        trade_resources = ""
        left_check = ""
        right_check = ""
        
        if card_name == "stage":
            trade_resources = self.stage["trade"]
        elif card_name in self.trade_cards:
            trade_resources = self.trade_cards[card_name]
           
        left_check = copy.deepcopy(trade_resources["left"])
        right_check = copy.deepcopy(trade_resources["right"])
        
        for r in trade_resources:
            for left_cost in left_check:
                while left_check[left_cost] > 0 and left_cost != "market" and left_cost != "post":
                    if right_check and right_check[left_cost] > 0:
                        right_check[left_cost] -= 1
                    left_check[left_cost] -= 1
                    needed_resources[left_cost] += 1
                    
            for right_cost in right_check:
                while right_check[right_cost] > 0 and right_cost != "market" and right_cost != "post":
                    right_check[right_cost] -= 1
                    needed_resources[right_cost] += 1
        
        left_check = copy.deepcopy(trade_resources["left"])
        right_check = copy.deepcopy(trade_resources["right"])
        
        check_resource = list([c[0] for c in [r for r in needed_resources.items()] if c[1] > 0])[0]
        is_rare = True if r in self.rare_resource else False
        trade_partner = self.get_trade_partner(left_check, right_check, check_resource, card_name, is_rare)
        
        check = self.trade_cards[card_name][trade_partner].copy()
        
        for r in needed_resources:    
            while needed_resources[r] > 0:
                if check[r] == 0:
                    is_rare = True if r in self.rare_resource else False
                    trade_partner = self.get_trade_partner(left_check, right_check, r, card_name, True if r in self.rare_resource else False)
                    check = self.trade_cards[card_name][trade_partner].copy()
                else:
                    needed_resources[r] -= 1
                    trade_cost = self.trade_cards[card_name][trade_partner]["post"]
                    if r in self.rare_resource:
                        trade_cost = self.trade_cards[card_name][trade_partner]["market"]
                        
                    if trade_partner == "left":
                        left_check[r] -= 1
                        left_coins += trade_cost
                    else:
                        right_check[r] -= 1
                        right_coins += trade_cost
        
        if left_coins > 0:
            self.is_trading_left = True
            self.left_coins = left_coins
        if right_coins > 0:
            self.is_trading_right = True
            self.right_coins = right_coins
                        
    def get_trade_partner(self, left, right, check, card_name, is_rare=False):
        left_none = True
        right_none = True
        
        if left[check] > 0:
            left_none = False
        if right[check] > 0:
            right_none = False
        
        trade_partner = "left"
        if is_rare:
            if self.trade_cards[card_name]["left"]["market"] == self.trade_cards[card_name]["right"]["market"] and (not left_none and not right_none):
                trade_partner = random.choice(["left", "right"])
            elif self.trade_cards[card_name]["left"]["market"] > self.trade_cards[card_name]["right"]["market"] or left_none:
                trade_partner = "right"
        else:
            if self.trade_cards[card_name]["left"]["post"] == self.trade_cards[card_name]["right"]["post"] and (not left_none and not right_none):
                trade_partner = random.choice(["left", "right"])
            elif self.trade_cards[card_name]["left"]["post"] > self.trade_cards[card_name]["right"]["post"] or left_none:
                trade_partner = "right"
        
        return trade_partner
    
    def view(self):
        print(f"(AI)")
        print(f"Name: {self.get_name()}")
        print(f"Board: {self.board.get_name()}")