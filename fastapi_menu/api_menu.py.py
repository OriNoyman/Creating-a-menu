from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union, Optional

app = FastAPI()

class SubOption(BaseModel):
    name: str
    description: Optional[str] = None
    action: str

class Option(BaseModel):
    name: str
    description: Optional[str] = None
    action: Union[str, List[SubOption]]

class Menu(BaseModel):
    id: int
    name: str
    options: List[Option] = []

menu = Menu(
    id=1,
    name="Main Menu",
    options=[]
)

class User(BaseModel):
    username: str
    password: str

users = []    

@app.get("/menu")
def get_menu():
    return menu

@app.post("/menu")
def create_menu(new_menu: Menu):
    global menu
    menu = new_menu
    return {"message": "Menu created successfully", "menu": menu}

@app.post("/menu/option")
def create_option(option: Option):
    if not menu.options:
        menu.options = []
    menu.options.append(option)
    return {"message": "Option created successfully", "menu": menu}

@app.put("/menu/option/{option_name}")
def update_option(option_name: str, updated_option: Option):
    for i, option in enumerate(menu.options):
        if option.name == option_name:
            menu.options[i] = updated_option
            return {"message": "Option updated successfully", "menu": menu}
    raise HTTPException(status_code=404, detail=f"Option '{option_name}' not found")

@app.delete("/menu")
def delete_menu():
    global menu
    menu = Menu(id=0, name="", options=[])
    return {"message": "Menu deleted successfully"}

@app.post("/signup")
def register_user(user: User):
    return sign_up(user)

@app.post("/menu/action/{option_name}")
def execute_action(option_name: str, sub_option_name: Optional[str] = None):
    for option in menu.options:
        if option.name == option_name:
            if isinstance(option.action, list):
                if sub_option_name:
                    for sub_option in option.action:
                        if sub_option.name == sub_option_name:
                            if sub_option.action in actions:
                                result = actions[sub_option.action]()
                                return {"message": f"Sub-option '{sub_option_name}' executed successfully", "result": result}
                    raise HTTPException(status_code=404, detail=f"Sub-option '{sub_option_name}' not found")
                return {"message": "Submenu found. Please choose a sub-option.", "submenu": option.action}
            elif isinstance(option.action, str):
                if option.action in actions:
                    result = actions[option.action]()
                    return {"message": f"Action '{option_name}' executed successfully", "result": result}
                else:
                    raise HTTPException(status_code=400, detail=f"Action '{option.action}' not found")
    
    raise HTTPException(status_code=404, detail=f"Option '{option_name}' not found")

def sign_up(user: User):
    for existing_user in users:
        if existing_user.username == user.username:
            raise HTTPException(status_code=400, detail="Username already exists")
        
    users.append(user)
    return {"message": "User registered successfully", "user": user}

def menu_action():
    print("Performs an action")

def exit_menu():
    print("Exiting the site")

def return_to_main_menu():
    global menu
    return {"message": "Returned to the main menu successfully", "menu": menu}

menu.options.append(
    Option(
        name="Login to the site",
        description="User login action",
        action="sign_up"
    )
)

menu.options.append(
    Option(
        name="Action in the site",
        description="Performs an action",
        action="menu_action"
    )
)

submenu_options = [
    SubOption(name="option one", description="Performs an action", action="menu_action"),
    SubOption(name="option two", description="Performs another action", action="menu_action"),
    SubOption(name="Return to the main menu", description="An action that returns to the main menu", action="return_to_main_menu"),
    SubOption(name="Exit", description="Exit the site", action="exit_menu")
]

menu.options.append(
    Option(
        name="Another menu",
        description="Opening another menu",
        action=submenu_options
    )
)

menu.options.append(
    Option(
        name="Exit",
        description="Exit the site",
        action="exit_menu"
    )
)

actions = {
    "sign_up": sign_up,  
    "menu_action": menu_action,
    "exit_menu": exit_menu, 
    "return_to_main_menu": return_to_main_menu
}
