import requests
import json

# The API endpoint URL
#This one would require web scraping to get the cookie to add to the header.
# url = "https://disneyworld.disney.go.com/dine-res/api/availability/3/2024-06-26,2024-06-26?facilityId=90002606;entityType=restaurant&entityType=restaurant"

#This one is a public API that doesn't require a cookie.
url = "https://disneyworld.disney.go.com/dining/dinemenu/api/menu?slug=boatwright-dining-hall&language=en-us"

print("Sending request to:", url)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

response = requests.get(url, headers=headers)

print("Received response")

# Check that the request was successful
if response.status_code == 200:
    print("Request was successful, parsing response")
    # Parse the JSON response
    data = json.loads(response.text)

    # Extract the reservation information
    # restaurants = data["restaurants"]
    # for date, reservations in restaurants.items():
    #     for reservation in reservations:
    #         print(f"Date: {date}")
    #         print(f"Meal Period: {reservation['mealPeriodType']}")
    #         print(f"Start Time: {reservation['startTime']}")
    #         print(f"End Time: {reservation['endTime']}")
    #         print(f"Cuisine: {reservation['cuisine']}")
    #         print(f"Service Style: {reservation['serviceStyle']}")
    #         for offer in reservation['offersByAccessibility'][0]['offers']:
    #             print(f"Offer Time: {offer['label']}")

    # Extract the menu information
    for meal_period in data["mealPeriods"]:
        for group in meal_period["groups"]:
            for item in group["items"]:
                for price in item["prices"]:
                    print(f"Menu Item: {item['title']}, Cost: {price['withoutTax']} {price['currency']}")
else:
    print(f"Request failed with status code {response.status_code}")