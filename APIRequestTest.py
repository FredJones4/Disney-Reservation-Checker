import requests
import json

# The API endpoint URL
url = "https://disneyworld.disney.go.com/dine-res/api/availability/3/2024-06-26,2024-06-26?facilityId=90002606;entityType=restaurant&entityType=restaurant"

print("Sending request to:", url)

# Make a GET request to the API
response = requests.get(url)

print("Received response")

# Check that the request was successful
if response.status_code == 200:
    print("Request was successful, parsing response")
    # Parse the JSON response
    data = json.loads(response.text)

    # Extract the reservation information
    restaurants = data["restaurants"]
    for date, reservations in restaurants.items():
        for reservation in reservations:
            print(f"Date: {date}")
            print(f"Meal Period: {reservation['mealPeriodType']}")
            print(f"Start Time: {reservation['startTime']}")
            print(f"End Time: {reservation['endTime']}")
            print(f"Cuisine: {reservation['cuisine']}")
            print(f"Service Style: {reservation['serviceStyle']}")
            for offer in reservation['offersByAccessibility'][0]['offers']:
                print(f"Offer Time: {offer['label']}")
else:
    print(f"Request failed with status code {response.status_code}")