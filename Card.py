class Card:
    def __init__(self,age,name,cost,build,product,color):
        self.age = age
        self.name = name
        self.cost = cost.split(',')
        self.build = build.split(',')
        self.product = product.split(',')
        self.color = color
        self.trade_cost = {"left":False,"right":False}
        self.is_available = False
    
    def view(self):
        print(f"Age: {self.get_age(True)}")
        print(f"Name: {self.get_name(True)}")
        print(f"Cost: {self.get_cost(True)}")
        print(f"Chain: {self.get_build(True)}")
        print(f"Product: {self.get_product(True)}")
        print(f"Color: {self.get_color(True)}")
        
    def set_cost(self, cost):
        self.cost = cost

    def get_age(self, view=False):
        return self.age
    
    def get_name(self, view=False):
        return self.name
    
    def get_cost(self, view=False):
        if(view):
            return self.list_view(self.cost)
        return self.cost
    
    def get_build(self, view=False):
        if(view):
            return ', '.join(self.build)
        return self.build
    
    def get_product(self, view=False):
        if(view):
            return self.list_view(self.product)
        return self.product
    
    def get_color(self, view=False):
        return self.color

    def list_view(self, list_to_view):
        list_dict = {}
        for x in list_to_view:
            if x in list_dict:
                list_dict[x] += 1
            else:
                list_dict[x] = 1
        list_view = ""
        for i, x in enumerate(list(list_dict.keys())):
            if x == "free" or x[:5] == "EVENT":
                list_view = x
            elif i == len(list_dict) - 1:
                list_view += (str(list_dict[x]) + " " + x)
            else:
                list_view += (str(list_dict[x]) + " " + x  + ", ")
        return list_view