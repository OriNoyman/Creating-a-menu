from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Union, Optional

app = FastAPI()

class SubOption(BaseModel):
    name: str
    description: Optional[str] = None
    action: Optional[str] = None

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
    options=[
        Option(
            name="option one",
            description="option one",
            action="action"
        ),
        Option(
            name="option two",
            description="sub menu",
            action=[
                SubOption(
                    name="sub option one",
                    description="sub option one",
                    action="action"
                ),
                SubOption(
                    name="sub option two",
                    description="sub option two",
                    action="action"
                )
            ]
        )
    ]
)


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
