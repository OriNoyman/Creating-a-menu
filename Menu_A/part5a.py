from abc import ABC, abstractmethod

class Menu(ABC):
    def __init__ (self, name):
        self.name = name

    @abstractmethod
    def execute(self):
        pass

class MenuAction(Menu):
    def __init__(self):
        super().__init__("Action in the site")

    def execute(self):
        print("the action in the progress")

class AnotherMenu(Menu):
    def __init__(self):
        super().__init__("Another menu")

    def execute(self):
        print("Opening another mute")

class Exit(Menu):
    def __init__(self):
        super().__init__("Exit")

    def execute(self):
        print("Exiting the menu")
        exit()

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
            try:
                self.show_options()
                choice = int(input("choose an option 1-3: "))
                if 1 <= choice <= len(self.items):
                   self.items[choice-1].execute()
                else:
                   print("Invalid option")
            except ValueError:
                print("please enter a valid number")       

def main():
    menu = MenuItem()
    menu.add_item(MenuAction())
    menu.add_item(AnotherMenu())
    menu.add_item(Exit()) 
    menu.run()

if __name__ == "__main__":
    main()               
