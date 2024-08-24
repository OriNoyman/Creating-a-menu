from abstract_menu import MenuItem, ActionMenuItem
from basic_menu import Menu
from utilities_functions import sign_up, menu_action, another_menu, exit_menu

def main():
    main_menu = Menu(name="Main Menu")
    main_menu.add_item(ActionMenuItem("Log in to the site", sign_up))
    main_menu.add_item(ActionMenuItem("Action in the site", menu_action))
    main_menu.add_item(ActionMenuItem("Opening another menu", lambda : another_menu(main_menu)))
    main_menu.add_item(ActionMenuItem("Exit", exit_menu))
    main_menu.run_menu()

if __name__ == "__main__":
    main()               
    