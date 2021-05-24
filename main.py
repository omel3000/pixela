import requests
from datetime import datetime


def confirm_user():
    global USER
    confirm_ans = input(f"Are you {USER}? (Y/N) ").upper()
    if confirm_ans == "EXIT":
        quit("Bye.. Bye...")
    if confirm_ans == "Y":
        return confirm_ans
    elif confirm_ans == "N":
        return confirm_ans
    else:
        confirm_user()


def confirm_new_user():
    confirm_ans = input(f"Do you have account? (Y/N) ").upper()
    if confirm_ans == "EXIT":
        quit("Bye.. Bye...")
    if confirm_ans == "Y":
        return confirm_ans
    elif confirm_ans == "N":
        return confirm_ans
    else:
        confirm_new_user()


def write_token():
    global TOKEN
    token_check = input("Write your token: ")
    if len(token_check) < 8 or len(token_check) > 128:
        print("Wrong token!\n"
              "minimum characters - 8\n"
              "maximum characters - 128")
        write_token()
    TOKEN = token_check


def write_user_data():
    global USER, TOKEN
    confirm_new_us = confirm_new_user()
    with open("user_data.txt", "w") as file:
        USER = input("Write your user name: ")
        write_token()
        us_data = f"{USER}\n{TOKEN}"
        file.write(us_data)
    if confirm_new_us == "N":
        create_new_user()


def create_new_user():
    global TOKEN, USER, pixela_endpoint
    user_params = {
        "token": TOKEN,
        "username": USER,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }
    create_new_us = requests.post(url=pixela_endpoint, json=user_params)
    response = create_new_us.json()
    if response["message"] == "Success.":
        print(response["message"])
    elif response["message"] == "This user already exist.":
        print(response["message"])
        write_user_data()

    else:
        print(response["message"])
        print("is done:", response["isSuccess"])


def colour_choice():
    COLOR = input("What color you want to use? (green, red, blue, yellow, purple, black): ").lower()
    if COLOR == "EXIT":
        quit("Bye.. Bye...")
    if COLOR == "red":
        return "momiji"
    elif COLOR == "green":
        return "shibafu"
    elif COLOR == "blue":
        return "sora"
    elif COLOR == "yellow":
        return "ichou"
    elif COLOR == "purple":
        return "ajisai"
    elif COLOR == "black":
        return "kuro"
    else:
        colour_choice()


def add_graph():
    global USER, TOKEN, pixela_endpoint
    headers = {
        "X-USER-TOKEN": TOKEN
    }
    endpoint = f"{pixela_endpoint}/{USER}/graphs"
    ID = input("Write ID: ")
    NAME = input("Write name: ")
    UNIT = input("What units do you want to use (e.g: km): ")
    COLOR = colour_choice()
    graph_config = {
        "id": ID,
        "name": NAME,
        "unit": UNIT,
        "type": "float",
        "color": COLOR
    }
    response = requests.post(url=endpoint, json=graph_config, headers=headers)
    response = response.json()
    if response["message"] == "Success.":
        print(response["message"])
    elif response["message"] == f"User `{USER}` does not exist or the token is wrong.":
        print(response["message"])
        write_user_data()
        add_graph()
    else:
        print(response["message"])
        print("is done:", response["isSuccess"])


def date_write():
    today_time = datetime.now()
    date_today = today_time.strftime("%Y%m%d")
    today = input("Today? (Y/N) ").upper()

    if today == "Y":
        return date_today
    elif today == "N":
        year = input("Year: ")
        month = input("Month: ")
        if len(month) == 1:
            month = f"0{month}"
        day = input("Day: ")
        if year == "EXIT":
            quit("Bye.. Bye...")
        if len(day) == 1:
            day = f"0{day}"
        DATE = f"{year}{month}{day}"
        try:
            if len(DATE) != 8 or int(month) > 12 or int(month) <= 0 or int(day) <= 0 or int(day) > 31 \
                    or int(DATE) > int(date_today):
                print("Wrong data! Try again!\n")
                date_write()
            else:
                return DATE
        except ValueError:
            print("Wrong data! Try again!\n")
            date_write()
    else:
        date_write()


def quantity_ans():
    QUANTITY = input("Quantity: ")
    return QUANTITY


def add_pixel():
    global USER, TOKEN, pixela_endpoint
    headers = {
        "X-USER-TOKEN": TOKEN
    }
    ID = input("ID of graph: ")
    link = f"{pixela_endpoint}/{USER}/graphs/{ID}"
    DATE = date_write()
    QUANTITY = quantity_ans()
    graph_add = {
        "date": DATE,
        "quantity": QUANTITY
    }
    response = requests.post(url=link, json=graph_add, headers=headers)
    response = response.json()
    if response["message"] == "Success.":
        print(response["message"])
    elif response["message"] == f"User `{USER}` does not exist or the token is wrong.":
        print(response["message"])
        write_user_data()
        add_pixel()
    else:
        print(response["message"])
        print("is done:", response["isSuccess"])


def what_do():
    print(f"What do you want to do?\n"
          f"1 - create graph\n"
          f"2 - add pixel to graph")
    do = input("Write number: ")
    if do == "1":
        add_graph()
    elif do == "2":
        add_pixel()


pixela_endpoint = "https://pixe.la/v1/users"
GAME_IS_ON = True


try:
    with open("user_data.txt", "r") as file:
        user_data = file.readlines()
        try:
            USER = user_data[0].replace("\n", "")
            TOKEN = user_data[1]
            confirm_us = confirm_user()
            if confirm_us == "Y":
                pass
            else:
                write_user_data()
        except IndexError:
            write_user_data()
except FileNotFoundError:
    write_user_data()

while GAME_IS_ON:
    what_do()
    game = input("Do you want exit? (Y/N) ").upper()
    if game == "Y":
        GAME_IS_ON = False
