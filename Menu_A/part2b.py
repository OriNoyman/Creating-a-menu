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
        for item in self.items:
            print(item.name)
    
    def free_text_menu(self):
        while True:
            self.show_options()
            choice = input("please choose a option: ")
            for item in self.items:
               if choice == item.name:
                  item.execute()     
            else:
                print("invalid option")
