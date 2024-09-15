from fastapi import FastAPI

app = FastAPI()

menu = {
    "id": 1,
    "name": "Main Menu",
    "options": [
        {
            "name": "option one",
            "description": "option one",
            "action": "action"
        },
        {
            "name": "option two",
            "description": "sub menu",
            "action": [
                {
                    "name": "sub option one",
                    "description": "sub option one",
                    "action": "action"
                },
                {
                    "name": "sub option two",
                    "description": "sub option two",
                    "action": "action"
                }
            ]
        }
    ]
}

@app.get("/menu")
def get_menu():
    return menu

@app.post("/menu")
def create_menu(new_menu: dict):
    global menu
    menu = new_menu
    return {"message": "Menu created successfully", "menu": menu}

@app.post("/menu/option")
def create_option(option: dict):
    if "options" not in menu:
        menu["options"] = []
    menu["options"].append(option)
    return {"message": "Option created successfully", "menu": menu}

@app.post("/menu/option/{option_name}/sub_option")
def add_sub_option(option_name: str, sub_option: dict):
    for option in menu.get("options", []):
        if option["name"] == option_name:
            if "sub_options" not in option:
                option["sub_options"] = []
            option["sub_options"].append(sub_option)
            return {"message": "Sub-option added successfully", "menu": menu}

@app.put("/menu/option/{option_name}")
def update_option(option_name: str, updated_option: dict):
    for i, option in enumerate(menu.get("options", [])):
        if option["name"] == option_name:
            menu["options"][i] = updated_option
            return {"message": "Option updated successfully", "menu": menu}

@app.delete("/menu")
def delete_menu():
    global menu
    menu = {}
    return {"message": "Menu deleted successfully"}
