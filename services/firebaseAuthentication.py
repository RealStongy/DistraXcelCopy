import pyrebase
import json
from services.singleton import UserData
import requests
import keyring
import jwt
import time

with open("firebaseConfiguration.json", "r") as f:
    firebaseConfig = json.load(f)

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()
API_KEY = firebaseConfig["apiKey"]
current_user = dict()


def signup(email, password):
    try:
        print("Attempting to create user...")
        user = auth.create_user_with_email_and_password(email, password)
        print(f"Success {user}")
        # user_dict = json.loads(user)
        db.child("users").child(f"{user['localId']}").update(
            {"accountType": "parent"})
        current_user = user
        return user
    except Exception as e:
        print(e)
        return None


def login(email, password):
    try:
        print("Attempting to login user...")
        user = auth.sign_in_with_email_and_password(email, password)
        print(f"Success {user}")
        current_user = user
        return user
    except Exception as e:
        print(e)
        return None


def logout():
    try:
        print("Attempting to logout user...")
        # user = auth.sign_out_with_email_and_password()
        print("Success")
        current_user = dict()
        return None
    except Exception as e:
        print(e)
        return None


def refresh_id_token(refresh_token):
    api_key = API_KEY
    refresh_url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"
    refresh_payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    response = requests.post(refresh_url, data=refresh_payload)
    id_token = response.json().get("id_token")
    return id_token


def get_valid_id_token():
    refresh_token = keyring.get_password("DistraXcel", "user_refresh_token")
    if not refresh_token:
        return None

    id_token = keyring.get_password("DistraXcel", "user_id_token")

    token = get_user_from_token(id_token)
    if token and token["exp"] < time.time():  # Handle expiration
        new_id_token = refresh_id_token(refresh_token)
        keyring.set_password("DistraXcel", "user_id_token", new_id_token)

        return new_id_token

    return id_token


def get_user_from_token(id_token):
    try:
        decoded_token = jwt.decode(id_token,
                                   options={"verify_signature": False})
        # print(f"Decoded Token: {decoded_token}")
        return decoded_token
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None


def start_firebase_listener(app, screens):

    def stream_handler(message):
        # Update the singleton
        user_data = UserData.get_instance().get_user_data()
        path_components = message["path"][1:].split("/")
        print(f"UPDATED STREAM MESSAGE: {message}")

        if path_components[0] == "categories":
            category_list = user_data["categories"]
            if len(path_components) > 1:
                category_list[int(path_components[1])] = message["data"]
            else:
                category_list = message["data"]
            user_data["categories"] = category_list
        elif path_components[0] == "settings":
            if path_components[1] == "pomodoro_rest_slider_val":
                user_data["settings"]["pomodoro_rest_slider_val"] = message[
                    "data"]
            elif path_components[1] == "pomodoro_work_slider_val":
                user_data["settings"]["pomodoro_work_slider_val"] = message[
                    "data"]

        UserData.get_instance().set_user_data(user_data)

        # Notify Screens
        app.queue.put(message)

    print(f"This is the current user: {app.uid}")

    if app.uid != "":
        print(f"Attempting stream for {app.uid}")
        app.user_stream = db.child(f"users/{app.uid}").stream(stream_handler)
