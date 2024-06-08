from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time as TIME
from twilio.rest import Client
import json
import os

# Selenium settings
TIMEOUT = 20
DISNEY_URL = 'https://disneyworld.disney.go.com/dining/polynesian-resort/ohana/'
DISNEY_EMAIL = 'fake.email099887@gmail.com'
DISNEY_PASSWORD = 'password123'

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
chrome_options.add_argument('--headless')  # Optional, run Chrome in headless mode
driver = webdriver.Chrome(options=chrome_options)

def get_settings():
    """Sets up the variables that Twilio API needs to send a text message"""
    if os.path.isfile("accounts.json"):
        json_data = open("accounts.json").read()
        data = json.loads(json_data)
    else:
        raise Exception("No 'accounts.json' file found")

    global account_sid, auth_token, twilio_number, to_numbers
    account_sid = data["account_sid"]
    auth_token = data["auth_token"]
    twilio_number = data["twilio_number"]
    to_numbers = data["to_phone_number"]

def login_to_disney(driver):
    try:
        # Open the calendar
        calendar_button_xpath = '//*[@id="finderDetailsContainer-90002606;entityType=restaurant"]/div[1]/finder-aag/div/div[2]/div/finder-button/a'
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, calendar_button_xpath))).click()

        # Enter email
        email_input_xpath = '//*[@id="InputIdentityFlowValue"]'
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, email_input_xpath))).send_keys(DISNEY_EMAIL)

        # Click continue
        continue_button_xpath = '//*[@id="BtnSubmit"]'
        driver.find_element(By.XPATH, continue_button_xpath).click()

        # Enter password
        password_input_xpath = '//*[@id="password"]'
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, password_input_xpath))).send_keys(DISNEY_PASSWORD)

        # Click sign-in
        sign_in_button_xpath = '//*[@id="dssLogin"]/div[2]/button'
        driver.find_element(By.XPATH, sign_in_button_xpath).click()
    except TimeoutException as e:
        print(f"Login failed: {e}")
        driver.quit()
        return False
    return True

def check_reservation(driver, party_size_xpath, date_xpath):
    try:
        # Select party size
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, party_size_xpath))).click()

        # Select date
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, date_xpath))).click()

        # Check availability
        search_button_xpath = '//*[@id="dineAvailSearchButton"]'
        driver.find_element(By.XPATH, search_button_xpath).click()

        time.sleep(3)  # Wait for the page to load

        # Check if reservations are available
        general_xpath = '/html/body/app-root/div/app-core-layout/div/div[2]/div/app-component-switcher/app-restaurant-details-date-range/div/section[2]/div'
        no_avail_xpath = '/html/body/app-root/div/app-core-layout/div/div[2]/div/app-component-switcher/app-restaurant-details-date-range/div/section[2]/div/div'

        if driver.find_element(By.XPATH, general_xpath).is_displayed():
            return True
        elif driver.find_element(By.XPATH, no_avail_xpath).is_displayed():
            return False
    except TimeoutException as e:
        print(f"Checking reservation failed: {e}")
        return False

def send_text_notification():
    client = Client(account_sid, auth_token)
    for number in to_numbers:
        message = client.messages.create(
            body="Hi, that reservation you wanted is available now!",
            from_=twilio_number,
            to=number
        )
        print(f"Message sent: {message.sid}")

def main():
    if login_to_disney(driver):
        party_size = 8  # Example party size
        party_size_xpath = f'//*[@id="count-selector{party_size}"]'
        date_xpath = '/html/body/app-root/div/app-core-layout/div/div[2]/div/app-component-switcher/app-restaurant-details-date-range/div/section[2]/app-search-range-availability-criteria/section[2]/div/div[1]/dpep-date-range-calendar-picker/div/div[1]/dpep-date-range-calendar/div/div[2]/table/tbody/tr[2]/td[4]/div/a'  # Example date (2024-08-07)

        while True:
            if check_reservation(driver, party_size_xpath, date_xpath):
                send_text_notification()
                with open('log.txt', 'a') as log_file:
                    log_file.write(f"Reservation available on 2024-08-07 for party size {party_size}\n")
                break
            else:
                print("No reservations available, checking again in 1 minute...")
                TIME.time.sleep(60)

    driver.quit()

if __name__ == "__main__":
    get_settings()  # set global variables for texting service
    main()
