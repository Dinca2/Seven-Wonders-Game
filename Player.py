import random
import Events as e
class Player:
    def __init__(self,name,board,ai=False):
        self.name=name
        self.board=board
        self.is_ai=ai
        
        self.hand={}
        self.available_cards = {}
        self.unavailable = {}
        
        self.stage = {"available":False, "trade":{}}
        
        self.resources={"wood":0,"stone":0,"brick":0,"ore":0,"glass":0,"silk":0,"paper":0,"coin":3, "any":0, "any_rare":0, "choice":{}}
        self.special_resources={"victory":0,"military":0,"cog":0,"compass":0,"tablet":0, "any_science":0, "tokens":{}}
        self.colors = {"brown":0, "white":0, "yellow":0, "grenn":0, "red":0, "blue":0,"purple":0}
        self.end_events = {}
        self.add_resources([board.get_start()], is_card=False)
        self.build = ["free", "none"]
        self.build_view = {}
        
        self.trade_cards = {}
        self.left_neighbor = ""
        self.right_neighbor = ""
        self.is_trading_left = False
        self.is_trading_right = False
        self.left_coins = 0
        self.right_coins = 0
        
    def set_hand(self,hand):
        self.available_cards = {}
        self.trade_cards = {}
        self.unavailable = {}
        self.left_coins = 0
        self.right_coins = 0
        self.hand = hand
        
    def set_left(self,player):
        self.left_neighbor = player
        
    def set_right(self,player):
        self.right_neighbor = player
    
    def set_action(self):
        card_name = ""
        action = 0
        stage_available = "not available"
        
        if not self.available_cards:
            self.available(self.hand)
            if self.stage["available"]:
                stage_available = "available"
        
        if not self.is_ai:
            self.view_hand()
            confirmed = False
            while not confirmed:
                print(f"""Select Action:\n1) play (card)\n2) discard (card)\n3) build wonder (card) ({stage_available})
                \n4) view hand\n5) view board\n6) view resources
                \n7) view {self.left_neighbor.get_name()}'s board (left)\n8) view {self.right_neighbor.get_name()}'s board (right)""")
                action = input()
                if not action.isnumeric() or int(action) > 8 or int(action) < 1:
                    print("please select action with 1, 2, 3, 4, 5, 6, 7 or 8")
                else:
                    action = int(action)
                    if action < 4:
                        confirmed, card_name = self.set_play_action(action)
                    elif action == 4:
                        self.view_hand()
                    elif action == 5:
                        self.board.view()
                    elif action == 6:
                        self.get_resources(view=True)
                    elif action == 7:
                        self.left_neighbor.board.view()
                        self.left_neighbor.get_resources(view=True)
                    elif action == 8:
                        self.right_neighbor.board.view()
                        self.right_neighbor.get_resources(view=True)

        else:
            if self.stage["available"] and len(self.hand) < 3:
                card_name = random.choice(list(self.hand))
                action = 3
            elif self.available_cards:
                card_name = random.choice(list(self.available_cards))
                action = 1 #play
            elif self.trade_cards:
                card_name = random.choice(list(self.trade_cards))
                action = 1 #trade
            else:
                card_name = random.choice(list(self.unavailable))
                action = 2
        
        return action, card_name
        
    def set_play_action(self, action):
        action_list = {1:"play", 2:"discard", 3:"build wonder"}
        valid = False
        conf_action = ""
        card_name = ""
        while not valid:
            if action == 1 and (not self.available_cards and not self.trade_cards):
                print("There are no available cards to play")
                return False, card_name
            if action == 1  or action == 2:
                card_name = input(f"what card do you want to {action_list[action]}? ")
                if card_name in self.hand:
                    if card_name in self.trade_cards and action == 1:
                        if self.confirm_trade(card_name):
                            conf_action = action_list[action] + " " + card_name
                            valid = True
                        else:
                            return False, card_name
                    elif card_name in self.unavailable and action == 1:
                        print(f"Not enough resources to {action_list[action]} {card_name}")
                    else:
                        conf_action = action_list[action] + " " + card_name
                        valid = True
                        
                
            elif action == 3:
                if self.stage["available"]:
                    if self.stage["trade"]:
                        self.confirm_trade("stage")
                    card_name = input(f"what card do you want to discard to build {self.board.get_stage()}? ")
                    conf_action = action_list[action] + "by discarding " + card_name
                    valid = True
                else:
                    print("Unable to build next wonder stage")
            if card_name not in self.hand:
                print("invalid card")
        
        confirmed = False
        while not confirmed:
            confirm = input(f"confirm action: {conf_action}? y/n ")
            if(confirm.lower() == "y" or confirm.lower() == "yes" or confirm == "1"):
                confirmed = True
                print("confirmed")
            elif confirm.lower() == "n" or confirm.lower() == "no" or confirm == "0":
                print("action canceled")
                return confirmed, card_name
            else:
                print("please respond with yes or no")
        
        return confirmed, card_name
            
    def play_card(self,action, card_name):
        card = self.hand[card_name]
        if action == 1:
            if card_name in self.available_cards or card_name in self.trade_cards:
                self.add_resources(card)
                if "coin" in card.get_cost(): # only time when resources are taken
                    for cost in card.get_cost():
                        if cost == "coin":
                            self.resources["coin"] -= 1
        elif action == 2:
            self.add_resources(["coin","coin","coin"], is_card=False)
        else:
            stage = self.board.get_stage()
            board_reward = self.board.get_stage_reward(stage)
            self.add_resources(board_reward, is_card=False)
            self.board.next_stage()
            self.stage["available"] = False
            self.stage["trade"] = {}
            
        del self.hand[card_name]
        return self.hand
    
    def activate_end_events(self):
        for event in self.end_events:
            params = self.end_events[event][0]
            e = self.end_events[event][1]
            e(*params)
            
    def confirm_trade(self, card_name):
        check = self.hand[card_name]
        left_neighbor = self.left_neighbor.get_name()
        right_neighbor = self.right_neighbor.get_name()
        rare_resource = ["glass","silk","paper"]
        needed_resources = {"wood":0,"stone":0,"brick":0,"ore":0,"glass":0,"silk":0,"paper":0}
        left_check = self.trade_cards[card_name]["left"].copy()
        right_check = self.trade_cards[card_name]["right"].copy()
        coin_check = self.resources["coin"]
        right_coins = 0
        left_coins = 0
        self.left_coins = 0
        self.right_coins = 0
        trade_resources = ""
        
        if card_name == "stage":
            trade_resources = self.stage["trade"]
        elif card_name in self.trade_cards:
            trade_resources = self.trade_cards[card_name]
        
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
                    
        left_check = self.trade_cards[card_name]["left"].copy()
        right_check = self.trade_cards[card_name]["right"].copy()
        trade_partners = {left_neighbor:left_check, right_neighbor:right_check} 
        trade_partner = ""
        if not self.is_ai:
            for r in needed_resources:
                while needed_resources[r] > 0:
                    print(f"You need to trade for {needed_resources[r]} more {r}")
                    picked = False
                    if left_check[r] > 0 and right_check[r] > 0:
                        print(f"{left_neighbor} has {left_check[r]} {r} and {right_neighbor} has {right_check[r]} {r}.")
                    elif left_check[r] > 0:
                        print(f"Only {left_neighbor} has {r} ({left_check[r]}).")
                        trade_partner = left_neighbor
                        picked = True
                    else:
                        print(f"Only {right_neighbor} has {r} ({right_check[r]}).")
                        trade_partner = right_neighbor
                        picked = True
                    
                    while not picked:
                        trade_partner = input(f"From whom do you want to trade one {r} from? {left_neighbor} or {right_neighbor}? (0 to cancel trade) ")
                        if trade_partner == left_neighbor or right_neighbor:
                            picked = True
                        elif trade_partner == "0": #cancel trade
                            print("trade canceled")
                            return False
                        elif trade_partner != left_neighbor and trade_partner != right_neighbor:
                            print(f"Can't recongnize {trade_partner}")
                        elif trade_partners[trade_partner][r] == 0:
                            print(f"{trade_partner} does not have enough {r} to trade. Pick other neighbor or cancel trade to reset")
                        
                    
                    
                    trade_cost = trade_partners[trade_partner]["post"]
                    if r in rare_resource:
                        trade_cost = trade_partners[trade_partner]["market"]
                    print(f"It costs {trade_cost} coins to trade from {trade_partner}")

                    if trade_cost > coin_check:
                        print(f"Not enough coins to trade. Pick other neighbor or cancel trade to reset")
                    else:
                        confirm = input(f"Confirm? type 1 to confirm. (You have {coin_check} coins) ")
                        if confirm == "1" and trade_cost <= self.resources["coin"]:
                            picked = True
                            coin_check -= trade_cost
                            needed_resources[r] -= 1
                            if trade_partner == left_neighbor:
                                left_check[r] -= 1
                                left_coins += trade_cost
                            else:
                                right_check[r] -= 1
                                right_coins += trade_cost
                        else:
                            print(f"trade unconfirmed")
                            return False

        else:
            trade_partner = self.get_trade_partner(left_check, right_check, card_name)
            check = self.trade_cards[card_name][trade_partner].copy()
            for r in needed_resources:    
                while needed_resources[r] > 0:
                    if check[r] == 0:
                        trade_partner = self.get_trade_partner(left_check, right_check, r, True if r in rare_resource else False)
                        check = self.trade_cards[card_name][trade_partner].copy()
                    else:
                        needed_resources[r] -= 1
                        trade_cost = self.trade_cards[card_name][trade_partner]["post"]
                        if r in rare_resource:
                            trade_cost = self.trade_cards[card_name][trade_partner]["market"]
                            
                        if trade_partner == "left":
                            left_check[r] -= 1
                            left_coins += trade_cost
                        else:
                            right_check[r] -= 1
                            right_coins += trade_cost
                    
        confirm_trade = False
        while not confirm_trade:
            confirm = "yes"
            if not self.is_ai:
                confirm = input(f"It will cost {left_coins + right_coins} coins to play {card_name}. 0 to cancel, anything else to confirm ")
            if confirm == "0": #cancel trade
                print("trade canceled")
                return False
            else:
                if left_coins > 0:
                    self.is_trading_left = True
                    self.left_coins = left_coins
                if right_coins > 0:
                    self.is_trading_right = True
                    self.right_coins = right_coins
                confirm_trade = True
        
        return True
    
    def get_trade_partner(self, left, right, check="", is_rare=False):
        left_none = True
        right_none = True
        
        if check:
            if left[check] > 0:
                left_none = False
            if right[check] > 0:
                right_none = False
        else:
            for r in left:
                if left[r] != 0:
                    left_none = False
        
        
        trade_partner = "left"
        if is_rare:
            if self.trade_cards[check]["left"]["market"] == self.trade_cards[check]["right"]["market"] and (not left_none and not right_none):
                trade_partner = random.choice(["left", "right"])
            elif self.trade_cards[check]["left"]["market"] > self.trade_cards[check]["right"]["market"] or left_none:
                trade_partner = "right"
        else:
            if self.trade_cards[check]["left"]["post"] == self.trade_cards[check]["right"]["post"] and (not left_none and not right_none):
                trade_partner = random.choice(["left", "right"])
            elif self.trade_cards[check]["left"]["post"] > self.trade_cards[check]["right"]["post"] or left_none:
                trade_partner = "right"
        
        return trade_partner
        
    def get_neighbor(self, neighbor = "left"):
        if neighbor == "left":
            return self.left_neighbor
        return self.right_neighbor
    
    def get_name(self):
        return self.name
    
    def get_resources(self, special=False, view=False):
    
        if view:
            print(f"{self.name}'s resources:")
            for r in self.resources:
                if not isinstance(self.resources[r],int) and len(self.resources[r]) != 0:
                    print(f"{r}: {self.resources[r]}")
                elif isinstance(self.resources[r],int) and self.resources[r] > 0:
                    print(f"{r}: {self.resources[r]}")
            print("")
            print(f"{self.name}'s special resources:")
            empty = True
            for r in self.special_resources:
                if not isinstance(self.special_resources[r],int) and len(self.special_resources[r]) != 0:
                    print(f"{r}: {self.special_resources[r]}")
                    empty = False
                elif isinstance(self.special_resources[r],int) and self.special_resources[r] > 0:
                    print(f"{r}: {self.special_resources[r]}")
                    empty = False
            if empty:
                print("none")
            
            if self.build_view:
                print("\nBuild chains: ")
                for build in self.build_view:
                    print(build + " -> ", end="")
                    print(', '.join(self.build_view[build]))
            print()
                
        if special:
            return self.special_resources        
        return self.resources
    
    def get_hand(self):
        return self.hand
    
    def get_color(self, color):
        return self.colors[color]
    
    def get_board(self):
        return self.board

    def is_ai(self):
        return self.is_ai
    
    def give_trade(self):
        if self.is_trading_left:
            self.left_neighbor.recieve_trade(self.left_coins,self.name)
        if self.is_trading_right:
            self.right_neighbor.recieve_trade(self.right_coins,self.name)
        self.resources["coin"] -= (self.left_coins + self.right_coins)
        self.is_trading_left = False
        self.is_trading_right = False
        
    def recieve_trade(self, coins, name):
        self.resources["coin"] += coins
        print(f"{self.name} recieved {coins} coins from {name}")
        
    def add_resources(self, resource, is_card=True, is_token=False):
        
        products = resource
        is_event = False
        if is_card and not is_token:
            products = resource.get_product()
            if resource.get_build()[0] != "none":
                self.build += resource.get_build()
                self.build_view[resource.get_name()] = resource.get_build()
            color = resource.get_color()
            if color in self.colors:
                self.colors[color] += 1
            else:
                self.colors[color] = 1
            event = ""
            event_name = ""
            if products[0][:5] == "EVENT":
                is_event = True
                event_name = products[0][6:]
                event = e.event_handler(event_name)
                event(self) #triggers/sets event
        
        if not is_event:
            for r in products:
                if r in self.resources:
                    self.resources[r]+=1
                elif r in self.special_resources:
                    self.special_resources[r]+=1
                elif is_token:
                    if r in self.special_resources["tokens"]:
                        self.special_resources["tokens"][r] += 1
                    else:
                        self.special_resources["tokens"][r] = 1                    
                elif "/" in r:
                    split = r.split('/')
                    choice = {split[0]:split[1]}
                    self.resources["choice"].update(choice)
                else:
                    self.special_resources[r] = "Built"
    
    def add_end_event(self, event_name, params, event):
        self.end_events[event_name] = [params,event]
        
    def available(self,hand):
        rare_resource = ["glass","silk","paper"]
        for card in hand:
            check = self.resources.copy()
            check["choice"] = self.resources["choice"].copy()
            available = True
            trade = {}
            card_cost = hand[card].get_cost().copy()
            if card not in self.build and "free" not in card_cost:
                for i,cost in enumerate(card_cost):
                    
                    if check[cost] > 0:
                        check[cost] -= 1
                        card_cost[i] = ""
                    elif cost in rare_resource and check["any_rare"] > 0:
                        check["any_rare"] -=1
                        card_cost[i] = ""
                    elif check["any"] > 0:
                        check["any"] -=1
                        card_cost[i] = ""
                    elif cost in check["choice"].keys():
                        card_cost[i] = ""
                        del check["choice"][cost]
                        
                    elif cost in check["choice"].values():
                        position = list(check["choice"].values()).index(cost)
                        key_list = list(check["choice"].keys())
                        key = key_list[position]
                        card_cost[i] = ""
                        del check["choice"][key]
                    else:
                        available = False
                        break
            
            if available:
                self.available_cards[card] = hand[card]
            else:
                card_cost = list(filter(None, card_cost))
                can_trade, trade = self.trade_available(card_cost)
                if can_trade:
                    self.trade_cards[card] = trade
                else:
                    self.unavailable[card] = hand[card]
        
        if not self.stage["available"]:
            self.stage_available()
        
        return self.available_cards, self.trade_cards, self.unavailable
    
    def trade_available(self, check):
        left_check = self.left_neighbor.get_resources().copy()
        right_check = self.right_neighbor.get_resources().copy()
        left_check["choice"] = self.left_neighbor.get_resources()["choice"].copy()
        right_check["choice"] = self.right_neighbor.get_resources()["choice"].copy()
        
        if len(left_check) == 0 or not isinstance(left_check, dict):
            print("ERROR")
            return
        if len(right_check) == 0 or not isinstance(right_check, dict):
            print("ERROR")
            return
        rare_resource = ["glass","silk","paper"]
        left_trade = {"market": 2,"post":2, "wood":0,"stone":0,"brick":0,"ore":0,"glass":0,"silk":0,"paper":0}
        right_trade = {"market": 2,"post":2, "wood":0,"stone":0,"brick":0,"ore":0,"glass":0,"silk":0,"paper":0}
        left_cost = 0
        right_cost = 0
        trade_cost = 0
        
        if "left trade" in self.special_resources:
            left_trade["post"] = 1
        if "right trade" in self.special_resources:
            right_trade["post"] = 1
        if "market" in self.special_resources:
            left_trade["market"] = 1
            right_trade["market"] = 1
        
        
        for cost in check:
            
            #can only trade for basic or rare resources and no coin
            if cost not in left_trade: 
                return False, {}
            
            if left_check[cost] > 0 and right_check[cost] > 0:
                left_check[cost] -= 1
                left_trade[cost] += 1
                right_trade[cost] += 1
            elif left_check[cost] > 0:
                left_check[cost] -= 1
                left_trade[cost] += 1
            elif right_check[cost] > 0:
                right_check[cost] -= 1
                right_trade[cost] += 1
            elif cost in left_check["choice"].keys() and cost in right_check["choice"].keys():
                left_trade[cost] += 1
                right_trade[cost] += 1
                del left_check["choice"][cost]
            elif cost in left_check["choice"].values() and cost in right_check["choice"].values():
                position = list(left_check["choice"].values()).index(cost)
                key_list = list(left_check["choice"].keys())
                key = key_list[position]
                left_trade[cost] += 1
                right_trade[cost] += 1
                del left_check["choice"][key]
            elif cost in left_check["choice"].keys():
                left_trade[cost] += 1
                del left_check["choice"][cost]
            elif cost in left_check["choice"].values():
                position = list(left_check["choice"].values()).index(cost)
                key_list = list(left_check["choice"].keys())
                key = key_list[position]
                left_trade[cost] += 1
                del left_check["choice"][key]
            elif cost in right_check["choice"].values():
                position = list(right_check["choice"].values()).index(cost)
                key_list = list(right_check["choice"].keys())
                key = key_list[position]
                right_trade[cost] += 1
                del right_check["choice"][key]
            elif cost in right_check["choice"].keys():
                right_trade[cost] += 1
                del right_check["choice"][cost]
            else:
                return False, {}
                
            if cost in rare_resource:
                left_cost = left_trade["market"]
                right_cost = right_trade["market"]
            else:
                left_cost = left_trade["post"]
                right_cost = right_trade["post"]
            
            #gets minimal trade cost
            if left_cost < right_cost:
                trade_cost += left_cost
            else:
                trade_cost += right_cost
            
            if trade_cost > self.resources["coin"]:
                return False, {}
            
        return True, {'left':left_trade, 'right':right_trade}
    
    def stage_available(self):
        check = self.resources.copy()
        available = True
        trade = {}
        stage_cost = self.board.get_stage_cost(self.board.get_stage()) 
        for i, cost in enumerate(stage_cost):
            if check[cost] > 0:
                check[cost] -= 1
                stage_cost[i] = ""
            else:
                available = False 
                break
        if available:
            self.stage["available"] = True
        else:
            stage_cost = list(filter(None,stage_cost))
            can_trade, trade = self.trade_available(stage_cost)
            self.stage["available"] = can_trade
            self.stage["trade"] = trade
    
    def view(self):
        human = "Human"
        if self.is_ai:
            human = "AI"
        print(f"({human})")
        print(f"Name: {self.get_name()}")
        print(f"Board: {self.board.get_name()}")
        
    def view_hand(self):
        view = True
        print(f"{self.name}'s hand: ")
        for name in self.hand:
            card = self.hand[name]
            available = "Not available"
            if name in self.available_cards:
                available = "Available"
            elif name in self.trade_cards:
                available = "Available through trade"
            print(f"{card.get_name(view)}:\n\tCost: {card.get_cost(view)} ({available})\n\tProduces: {card.get_product(view)}\n\tChain: {card.get_build(view)}")
        