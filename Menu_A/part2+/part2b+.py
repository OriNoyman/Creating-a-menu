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
def main():
    menu = MenuItem()
    menu.add_item(MenuAction())
    menu.add_item(AnotherMenu())
    menu.add_item(Exit()) 
    menu.free_text_menu()

if __name__ == "__main__":
    main()               
           
