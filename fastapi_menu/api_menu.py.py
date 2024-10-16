from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional

from table_definition import Base, Menu, MenuItem, MenuOption, User, MenuAction

SQLALCHEMY_DATABASE_URL = 'mssql+pyodbc://sa:OriDbMenu123@localhost:1433/TableDefinition?driver=ODBC+Driver+17+for+SQL+Server'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MenuValidation(BaseModel):
    name: str
    parent_menu_id: Optional[int] = None
    
class MenuItemValidation(BaseModel):
    name: str
    menu_id: int

class MenuOptionValidation(BaseModel):
    menu_id: int
    action_id: Optional[int] = None

class MenuActionValidation(BaseModel):
    action_name: str
    description: Optional[str]

class UserValidation(BaseModel):
    username: str
    password: str    

@app.post("/menus/")
def create_menu(menu: MenuValidation, db: Session = Depends(get_db)):
    db_menu = Menu(name=menu.name)
    if menu.parent_menu_id:
        parent_menu = db.query(Menu).filter(Menu.id == menu.parent_menu_id).first()
        if not parent_menu:
            raise HTTPException(status_code=404, detail="Parent menu not found")
        db_menu.parent_menu = parent_menu
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu

@app.post("/menu_items/")
def create_menu_item(menu_item: MenuItemValidation, db: Session = Depends(get_db)):
    db_menu_item = MenuItem(name=menu_item.name, menu_id=menu_item.menu_id)
    db.add(db_menu_item)
    db.commit()
    db.refresh(db_menu_item)
    return db_menu_item

@app.post("/menu_options/")
def create_option(menu_option: MenuOptionValidation, db: Session = Depends(get_db)):
    db_menu_option = MenuOption(menu_id=menu_option.menu_id, action_id=menu_option.action_id)
    db.add(db_menu_option)
    db.commit()
    db.refresh(db_menu_option)
    return db_menu_option

@app.put("/menu_options/{option_id}")
def update_option(option_id: int, updated_option: MenuOptionValidation, db: Session = Depends(get_db)):
    db_update_option = db.query(MenuOption).filter(MenuOption.id == option_id).first()
    if not db_update_option:
        raise HTTPException(status_code=404, detail="MenuOption not found")
    db_update_option.menu_id = updated_option.menu_id
    db_update_option.action_id = updated_option.action_id
    db.commit()
    db.refresh(db_update_option)
    return db_update_option

@app.post("/menu_actions/")
def create_action(menu_action: MenuActionValidation, db: Session = Depends(get_db)):
    db_menu_action = MenuAction(action_name=menu_action.action_name, description=menu_action.description)
    db.add(db_menu_action)
    db.commit()
    db.refresh(db_menu_action)
    return db_menu_action

@app.delete("/menus/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu_to_delete = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu_to_delete is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    db.delete(menu_to_delete)
    db.commit()
    return menu_to_delete

@app.post("/users/")
def sign_up_user(user: UserValidation, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        if existing_user.password != user.password:
           raise HTTPException(status_code=404, detail="Invalid username or password")
        return {"message": f"Login successful. Welcome, {existing_user.username}!"}
    else:
        if not user.username or not user.password:
            raise HTTPException(status_code=404, detail="Username and password are required for registration")       
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
POST /menu_actions/
{
    "action_name": "Action",
    "description": "action in the main menu"
}

@app.post("/menu_options/perform/{option_id}")
def perform_menu_option(option_id: int, db: Session = Depends(get_db)):
    option = db.query(MenuOption).filter(MenuOption.id == option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Menu option not found")
    action = db.query(MenuAction).filter(MenuAction.id == option.action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    return {"message": f"Action '{action.action_name}' performed successfully!"}

POST /menu_actions/

{
    "action_name": "Exit",
    "description": "Exit the system"
}

@app.post("/menu_options/perform/{option_id}")
def perform_menu_option(option_id: int, db: Session = Depends(get_db)):
    option = db.query(MenuOption).filter(MenuOption.id == option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Menu option not found")
    action = db.query(MenuAction).filter(MenuAction.id == option.action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    if action.action_name.lower() == "exit":
        return {"message": "Exiting the system. Goodbye!"}
    return {"message": f"Action '{action.action_name}' performed successfully!"}

POST /menus/

{
    "name": "Sub Menu",
    "parent_menu_id": 1 
}


action_routes = {
    "sign_up": "/users/",
    "exit": "/menu-actions/",
    "sub_menu": "/menus/"
}

submenu_options = {
    "Back to the main menu": "/menu/{menu_id}",
    "perform_action": "/menu-options/perform/{option_id}"
}

@app.put("/menus/{menu_id}/add_options")
def add_menu_options(menu_id: int, db: Session = Depends(get_db)):
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    for action_name, action_route in action_routes.items():
        db_menu_item = MenuItem(name=action_name, menu_id=db_menu.id, action_route=action_route)
        db.add(db_menu_item)

    for option_name, option_route in submenu_options.items():
        db_menu_item = MenuItem(name=option_name, menu_id=db_menu.id, action_route=option_route)
        db.add(db_menu_item)

    db.commit()

@app.get("/menu/{menu_id}")
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(Menu).get(menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    menu_items = [name for name in action_routes.keys()] 
    return {"menu": menu, "menu_items": menu_items}

@app.get("/menu/submenu/{menu_id}")
def get_sub_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = db.query(Menu).get(menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    submenu_items = list(submenu_options.keys())
    return {"menu": menu, "submenu_items": submenu_items}

@app.post("/menu/choose/")
def choose_option(option_name: str):
    if option_name not in action_routes and option_name not in submenu_options:
        raise HTTPException(status_code=404, detail="Option not found")
    
    if option_name in action_routes:
        action_route = action_routes[option_name]
    else:
        action_route = submenu_options[option_name]
    return {"message": f"Action '{option_name}' initiated. Route: {action_route}"}
