class Board:
    def __init__(self,name,start,num_stages,costs,rewards,time):
        self.name = name.iloc[0]
        self.start = start
        self.num_stages = int(num_stages.iloc[0])
        self.costs = costs.to_string(index=False).split("-")
        self.rewards = self.set_rewards(rewards)
        self.time = time.to_string(index=False)
        self.stage = 0
        
    def view(self):
        print(f"{self.name}")
        print(f"Starting resource: {self.start.to_string(index=False)}")
        print(f"Time: {self.time}")
        for x in range(1,self.num_stages + 1):
            built = ""
            if self.stage >= x:
                built = " (built)"
            print(f"Stage {x}{built}: \n\tCost: {self.get_stage_cost(x - 1, view=True)}\n\tReward: {self.get_stage_reward(x - 1, view=True)}")
                
        
    def get_stage(self,view=False):
        return self.stage
    
    def get_start(self):
        return self.start.to_string(index=False)
    
    def get_stage_cost(self,stage, view=False):
        if(view):
            return ', '.join(self.costs[stage].split(","))
        return self.costs[stage].split(",")
    
    def get_stage_reward(self,stage, view=False):
        if(view):
            return ', '.join(self.rewards[stage].split(","))
        return self.rewards[stage].split(",")
    
    def get_name(self):
        return self.name
    
    def next_stage(self):
        if self.stage < 2:
            self.stage += 1
    
    def set_rewards(selfm,rewards):
        rewards = rewards.to_string(index=False).split("-")

        for i,r in enumerate(rewards):
            num_victory = 0
            num_coin = 0
            if r[:2] == "vp":
                num_victory = int(r[2])
            vp = ""
            for victory in range(0,num_victory-1):
                vp = vp + "victory,"
            if vp:
                vp = vp + "victory"
                rewards[i] = vp
            if r[:2] == "au":
                num_coin = int(r[2])
            au = ""
            for coin in range(0,num_coin-1):
                au = au + "coin,"
            if au:
                au = au + "coin"
                rewards[i] = au
        return rewards
