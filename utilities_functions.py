from abstract_menu import MenuItem, ActionMenuItem
from basic_menu import Menu

def sign_up():
    personal_details = input("Please enter your personal details separated by commas: ")
    inputs = personal_details.split(",")
    
    all_the_details = [] 
    for value in inputs:
        value = value.strip()
        try:
            all_the_details.append(int(value)) 
        except ValueError:
            try:
               all_the_details.append(float(value)) 
            except ValueError:
               all_the_details.append(value) 

    print(all_the_details)

def menu_action():
    print("Performs an action")

def another_menu(main_menu):
    sub_menu = Menu(name="sub menu")
    
    sub_menu.add_item(ActionMenuItem("option one", menu_action))
    sub_menu.add_item(ActionMenuItem("option two", menu_action))
    sub_menu.add_item(ActionMenuItem("Return to the main menu", lambda: main_menu.run()))
    sub_menu.add_item(ActionMenuItem("Exit", exit_menu))   

    sub_menu.run_menu()

def exit_menu():
    print("Exiting the site")
    exit()                     
