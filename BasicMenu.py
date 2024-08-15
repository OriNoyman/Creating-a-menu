from AbstractMenu import MenuItem, ActionMenuItem
from typing import List

class Menu:
    def __init__(self, name = "Main Menu"):
        self.name = name
        self.items : List[MenuItem] = []
        self.running = True

    def add_item(self, item : MenuItem):
        self.items.append(item)
    
    def show_options(self):
        print(f"-- {self.name} --")
        for i, item in enumerate(self.items, 1):
            print(f"{i} - {item.name}")

    def choose_menu_type(self):
        while True:
            self.menu_type = input("choose menu type ('number' or 'text'): ").lower()
            if self.menu_type in ['number', 'text']:
                break 
            else:
                print("Invalid option. Please choose 'number' or 'text': ")
    
    def run(self):
        while self.running:
            try:
                self.show_options()
                if self.menu_type == 'number':
                    choice = int(input("choose an option 1-4: "))
                    if 1 <= choice <= len(self.items):
                        self.items[choice-1].execute()
                        self.stop()
                    else:
                        print("Invalid option, please enter a valid number")
                
                elif self.menu_type == 'text': 
                    choice = input("choose an option: ")
                    found = False
                    for item in self.items:
                        if choice == item.name:
                            found = True
                            item.execute()
                            self.stop()
                            break 
                    if not found:
                            print("Invalid option, please try again")
            
            except ValueError:
                print("Invalid option. please enter a valid option.")

    def stop(self):
        self.running = False        
