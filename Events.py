import copy

def event_handler(event, expansions = ["base"]):
    #if ____ in expansion:
    #   events = ...
    #else:
    events = {"brown_coin":brown_coin,
              "brown_victory":brown_victory,
              "yellow_victory":yellow_victory,
              "white_victory":white_victory,
              "arena":arena,
              "brown_neighbor_victory":brown_neighbor_victory,
              "white_neighbor_victory":white_neighbor_victory,
              "yellow_neighbor_victory":yellow_neighbor_victory,
              "green_neighbor_victory":green_neighbor_victory,
              "red_neighbor_victory":red_neighbor_victory,
              "blue_neighbor_victory":blue_neighbor_victory,
              "defeat_neighbor":defeat_neighbor,
              "ship_guild":ship_guild,
              "science_guild":science_guild,
              "wonder_built":wonder_built,
              "play_discard":play_discard,
              "olympia_special_a":olympia_special_a,
             #"olympia_special_b":olympia_special_b
             }
    
    return events[event]
    

def get_num_color(player, color, neighbors=["left", "right"], only_neighbors = False):
    num_color = 0
    if neighbors:
        for neighbor in neighbors:
            num_color += player.get_neighbor(neighbor).get_color(color)
    
    if only_neighbors:
        return num_color
    
    num_color += player.get_color(color)
    return num_color

def get_num_token(player, token, neighbors=["left", "right"], only_neighbors = False):
    num_token = 0
    if neighbors:
        for neighbor in neighbors:
            num_token += player.get_neighbor(neighbor).get_resources()["tokens"][token]
    
    if only_neighbors:
        return num_token
    
    num_token += player.get_resources()["tokens"][token]
    return num_token
    
def brown_coin(player):
    num_brown = get_num_color(player,"brown")
    coins = []
    for i in range(0,num_brown):
        coins.append("coin")
    player.add_resources(coins, is_card = False)
    
def brown_victory(player, get_coins=True):
    num_brown = get_num_color(player,"brown",neighbors=[])
    coins = []
    victory = []
    for i in range(0,num_brown):
        coins.append("coin")
        victory.append("victory")
    if get_coins:
        player.add_resources(coins, is_card = False)
        player.add_end_event("brown_victory",(player,False),brown_victory)
    else:
        player.add_resources(victory, is_card = False)
    
def yellow_victory(player, get_coins=True):
    num_yellow = get_num_color(player,"yellow",neighbors=[])
    coins = []
    victory = []
    for i in range(0,num_yellow):
        coins.append("coin")
        victory.append("victory")
    if get_coins:
        player.add_resources(coins, is_card = False)
        player.add_end_event("yellow_victory",(player,False),yellow_victory)
    else:
        player.add_resources(victory, is_card = False)

def white_victory(player, get_coins=True):
    num_white = get_num_color(player,"white",neighbors=[])
    coins = []
    victory = []
    for i in range(0,num_white):
        coins.append("coin")
        coins.append("coin")
        victory.append("victory")
        victory.append("victory")
    if get_coins:
        player.add_resources(coins, is_card = False)
        player.add_end_event("white_victory",(player,False),white_victory)
    else:
        player.add_resources(victory, is_card = False)
        
def arena(player):
    num_complete_stages = player.get_board().get_stage()
    coins = []
    victory = []
    for n in range(0,num_complete_stages):
        coins.append("coin")
        coins.append("coin")
        coins.append("coin")
        victory.append("victory")
    player.add_resources(coins, is_card = False)
    player.add_resources(victory, is_card = False)

def brown_neighbor_victory(player, end=False):
    if end:
        num_brown = get_num_color(player,"brown",only_neighbors=True)
        victory = []
        for n in range(0,num_brown):
            victory.append("victory")
        player.add_resources(victory, is_card = False)
    else:
        player.add_end_event("workers guild",(player,True),brown_neighbor_victory)

def white_neighbor_victory(player, end=False):
    if end:
        num_white = get_num_color(player,"white",only_neighbors=True)
        victory = []
        for n in range(0,num_white):
            victory.append("victory")
            victory.append("victory")
        player.add_resources(victory, is_card = False)
    else:
        player.add_end_event("craftsman guild",(player,True),white_neighbor_victory)

def yellow_neighbor_victory(player, end=False):
    if end:
        num_yellow = get_num_color(player,"yellow",only_neighbors=True)
        victory = []
        for n in range(0,num_yellow):
            victory.append("victory")
        player.add_resources(victory, is_card = False)
    else:
        player.add_end_event("traders guild",(player,True),yellow_neighbor_victory)
        
def green_neighbor_victory(player, end=False):
    if end:
        num_green = get_num_color(player,"green",only_neighbors=True)
        victory = []
        for n in range(0,num_green):
            victory.append("victory")
        player.add_resources(victory, is_card = False)
    else:
        player.add_end_event("philosophers guild",(player,True),green_neighbor_victory)
        
def red_neighbor_victory(player, end=False):
    if end:
        num_red = get_num_color(player,"red",only_neighbors=True)
        victory = []
        for n in range(0,num_red):
            victory.append("victory")
        player.add_resources(victory, is_card = False)
    else:
        player.add_end_event("builders guild",(player,True),red_neighbor_victory)
        
def defeat_neighbor(player, end=False):
    if end:
        num_token = get_num_token(player,"defeat",only_neighbors=True)
        victory = []
        for n in range(0,num_token):
            victory.append("victory")
        player.add_resources(victory, is_card = False)
    else:
        player.add_end_event("strategy guild",(player,True),defeat_neighbor)
        
def ship_guild(player, end=False):
    if end:
        num_brown = get_num_color(player,"brown",neighbors=[])
        num_white = get_num_color(player,"white",neighbors=[])
        num_purple = get_num_color(player,"purple",neighbors=[])
        
        total = num_brown + num_white + num_purple
        victory = []
        for n in range(0,total):
            victory.append("victory")
        player.add_resources(victory, is_card = False)
    else:
        player.add_end_event("shipowners guild",(player,True),ship_guild)
        
def science_guild(player, end=False):
        player.add_resources(["any_science"], is_card=False)
        
def blue_neighbor_victory(player, end=False):
    if end:
        num_blue = get_num_color(player,"blue",only_neighbors=True)
        victory = []
        for n in range(0,num_blue):
            victory.append("victory")
        player.add_resources(victory, is_card = False)
    else:
        player.add_end_event("magistrates guild",(player,True),blue_neighbor_victory)
        
def wonder_built(player, end=False):
    if end:
        num_complete_stages = player.get_board().get_stage()
        num_complete_stages += player.get_neighbor("left").get_board().get_stage()
        num_complete_stages += player.get_neighbor("right").get_board().get_stage()
        victory = []
        for n in range(0,num_complete_stages):
            victory.append("victory")
        
        player.add_resources(victory, is_card = False)
    else:
        player.add_end_event("builders guild",(player,True),wonder_built)
        
def play_discard(player):
    discarded_cards = player.get_discard()
    if not discarded_cards:
        print("unfortuently, there are no cards in the discard pile")
        return
    old_hand = copy.deepcopy(player.get_hand())
    player.set_hand(discarded_cards)
    player.set_available(discarded_cards)
    confirmed = False
    card_name = ""
    print(f"{player.get_name()} please select a card to play from the discard pile.")
    while not confirmed:
        player.view_hand()
        confirmed, card_name = player.set_play_action(1)
    
    player.play_card(1,card_name)
    player.set_hand(old_hand)
    
def olympia_special_a(player, end=False):
    if not end:
        player.add_end_event("olympia_special_a",(player, True),olympia_special_a)
        print(f"olympia special_________{player.end_events}")