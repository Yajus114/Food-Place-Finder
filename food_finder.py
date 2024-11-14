import requests
import json
from urllib.parse import urlencode


def get_category_ids(cats, choices):
    res: str = ""
    for cat in cats.split(","):
        res += process.extract(cat, choices, scorer=fuzz.WRatio, limit=1)[0][0][:5] + ","
    return res[:-1]


if __name__ == "__main__":
    url: str = "https://api.foursquare.com/v3/places/search?"
    params: dict = {}

    with open("Food Places App API Key 1.txt", "r") as file:
        api_key: str = file.readline().strip()

    headers: dict = {
        "accept": "application/json",
        "Authorization": api_key,
    }

    params["query"] = input("Enter the details: ")
    params["near"] = input("Enter the locality (e.g. Gurgaon, Haryana): ")
    params["limit"] = input("Enter: ") if input("Enter how many responses you want to receive (default = 5) (y/n): ") == "y" else "5"

    if input("Would you like to input categories manually? (y/n): ") == "y":
        from rapidfuzz import fuzz, process

        with open("categories_list.txt", "r") as choices_file:
            choices: list = choices_file.read().splitlines()
            cats: str = input("Enter the specific categories (comma separated): ")
            params["categories"] = get_category_ids(cats, choices)

    response = requests.get(url + urlencode(params), headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        for place in data.get("results", []):
            name: str = place.get("name")
            address: str = place.get("location", {}).get("formatted_address")
            print(f"Name: {name}\nAddress: {address}\n")
    else:
        print(f"Request failed with status code: {response.status_code}")
