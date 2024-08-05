from abc import ABC, abstractmethod

class Menu(ABC):
    def __init__ (self, name):
        self.name = name

    @abstractmethod
    def execute(self):
        pass
    
class MenuItem:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
    
    def show_options(self):
        print("-- Main Menu --")
        for i, item in enumerate(self.items, 1):
            print(f"{i} - {item.name}")

    def run(self):
        while True:
            self.show_options()
            try:
                choice = int(input("choose an option 1-3: "))
                if 1 <= choice <= len(self.items):
                   self.items[choice-1].execute()
                else:
                   print("invalid option")
            except ValueError:
                print("Invalid selection, please try again")    
                
