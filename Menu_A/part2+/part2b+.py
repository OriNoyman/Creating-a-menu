from abc import ABC, abstractmethod

class Menu(ABC):
    def __init__ (self, name):
        self.name = name

    @abstractmethod
    def execute(self):
        pass

class OptionOne(Menu):
    def __init__(self):
        super().__init__("Option One")

    def execute(self):
        print("Empty Option")

class OptionTwo(Menu):
    def __init__(self):
        super().__init__("Use This Option")

    def execute(self):
        print("Good Option")

class MenuItem:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
    
    def show_options(self):
        print("-- Free text menu --")
        for item in self.items:
            print(item.name)
    
    def free_text_menu(self):
        while True:
            self.show_options()
            choice = input("Choose from the following option: ")
            for item in self.items:
               if choice == item.name:
                  item.execute()     
            else:
                print("invalid option")
                
def main():
    menu = MenuItem()
    menu.add_item(OptionOne())
    menu.add_item(OptionTwo()) 
    menu.free_text_menu()

if __name__ == "__main__":
    main()               
           
