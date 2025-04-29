import requests
from datetime import datetime

#sheety api configs
SHEETY_API_ENDPOINT = "https://api.sheety.co/3173a0ef8ce49203f5444de4f27f54fa/myWorkouts/workouts"
SHEETY_API_TOKEN = "" #if enabled

#sheety api configs and authentication
NUTRITIONIX_API_ID = "" #your nutritionix id
NUTRITIONIX_API_KEY = "" #your nutritionix api
nutritionix_headers = {
    "x-app-id": NUTRITIONIX_API_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
    "Content-Type": "application/json"
}

#user inputs here their daily exercise information
description = input("Which exercises have you practiced today?")
gender = input("What's your gender (male/female?")
weight = input(float("What's your weight (in kilograms)?"))
height = input(int("What's your height (in centimeters)?"))
age = input(int("What's your age?"))

#form for posting user info
body = {
    "query": description,
    "gender": gender,
    "weight_kg": weight,
    "height_cm": height,
    "age": age
}

#getting data from nutritionix api
response = requests.post(
    url="https://trackapi.nutritionix.com/v2/natural/exercise",
    json=body,
    headers=nutritionix_headers
)

data = response.json()

#obtaining current date and time in readable formats
today = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%H:%M:%S")

#transpositioning data to google sheets file via sheety
for exercise in data["exercises"]:
    workout_data = {
        "workout": {
            "date": today,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    response = requests.post(
        url=SHEETY_API_ENDPOINT,
        json=workout_data,
    )
    print(response.text)

