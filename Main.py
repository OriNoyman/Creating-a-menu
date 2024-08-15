from AbstractMenu import MenuItem, ActionMenuItem
from BasicMenu import Menu
from UtilitiesFunctions import sign_up, menu_action, another_menu, exit_menu

def main():
    menu = Menu(name="Main Menu")
    menu.add_item(ActionMenuItem("Log in to the site", sign_up))
    menu.add_item(ActionMenuItem("Action in the site", menu_action))
    menu.add_item(ActionMenuItem("Opening another menu", another_menu))
    menu.add_item(ActionMenuItem("Exit", exit_menu))
    menu.choose_menu_type()
    menu.run()

if __name__ == "__main__":
    main()               