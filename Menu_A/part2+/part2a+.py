from abc import ABC, abstractmethod

class Menu(ABC):
    def __init__ (self, name):
        self.name = name

    @abstractmethod
    def execute(self):
        pass
    
class OptionOne(Menu):
    def __init__(self):
        super().__init__("Option one")

    def execute(self):
        print("option one")

class OptionTwo(Menu):
    def __init__(self):
        super().__init__("Some other option")

    def execute(self):
        print("Some other option")

class OptionTree(Menu):
    def __init__(self):
        super().__init__("Good option")

    def execute(self):
        print("Option tree")

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

def main():
    menu = MenuItem()
    menu.add_item(OptionOne())
    menu.add_item(OptionTwo())
    menu.add_item(OptionTree()) 
    menu.run()

if __name__ == "__main__":
    main()               
           
