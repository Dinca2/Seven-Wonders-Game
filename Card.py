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
            return ', '.join(self.cost)
        return self.cost
    
    def get_build(self, view=False):
        if(view):
            return ', '.join(self.build)
        return self.build
    
    def get_product(self, view=False):
        if(view):
            products = {}
            for p in self.product:
                if p in products:
                    products[p] += 1
                else:
                    products[p] = 1
            product_view = ""
            for i, p in enumerate(list(products.keys())):
                if i == len(products) - 1:
                    product_view += (str(products[p]) + " " + p)
                else:
                    product_view += (str(products[p]) + " " + p  + ", ")
            return product_view
        return self.product
    
    def get_color(self, view=False):
        return self.color
