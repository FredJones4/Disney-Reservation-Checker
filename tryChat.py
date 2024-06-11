import time as TIME
import sched
from datetime import datetime

# Other necessary imports for selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

TIMEOUT = 20  # Increase timeout
DISNEY_URL = 'https://disneyworld.disney.go.com/dining/polynesian-resort/ohana/'
DISNEY_EMAIL = 'fake.email099887@gmail.com'
DISNEY_PASSWORD = 'password123'

scheduler = sched.scheduler(TIME.time, TIME.sleep)

def close_overlay(driver):
    try:
        overlay_xpath = '//*[@id="sec-overlay"]'
        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, overlay_xpath)))
        driver.execute_script("document.getElementById('sec-overlay').style.display = 'none';")
        print("Overlay closed.")
    except TimeoutException:
        print("No overlay found.")
        pass

def check_xpath_exists(driver, xpath):
    try:
        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return True
    except (NoSuchElementException, TimeoutException):
        return False

def make_reservation():
    driver = webdriver.Chrome()

    driver.get(DISNEY_URL)

    # Add implicit wait
    driver.implicitly_wait(10)

    # Open the calendar
    try:
        calendar_button_xpath = '//*[@id="finderDetailsContainer-90002606;entityType=restaurant"]/div[1]/finder-aag/div/div[2]/div/finder-button/a'
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, calendar_button_xpath))).click()

    except TimeoutException:
        print("Couldn't load calendar button")
        driver.quit()
        return False

    # Sign in
    try:
        # Enter email
        iframe = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.ID, 'oneid-iframe'))
        )
        driver.switch_to.frame(iframe)
        print("Switched to iframe.")

        # Enter email
        email_field = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located((By.ID, 'InputIdentityFlowValue'))
        )
        print("Email field found.")

        # Enter the email
        email_field.send_keys(DISNEY_EMAIL)
        print("Email entered.")

        continue_button = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, 'BtnSubmit'))
        )
        continue_button.click()
        print("Continue button clicked.")
    except TimeoutException:
        print("Couldn't find email field or continue button")
        driver.quit()
        return False

    try:
        # Enter password
        password_input_xpath = '//*[@id="InputPassword"]'
        password_element = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, password_input_xpath)))
        password_element.click()
        password_element.send_keys(DISNEY_PASSWORD)

        # Click sign-in
        sign_in_button_xpath = '//*[@id="BtnSubmit"]'  # '//*[@id="dssLogin"]/div[2]/button'
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath))).click()

    except TimeoutException:
        print("Couldn't sign in")
        driver.quit()
        return False

    # Add implicit wait
    TIME.sleep(30)

    try:
        # Group Size Try 2
        TIME.sleep(5)
        # Close any overlays if present
        close_overlay(driver)

        group_size_2 = '//*[@id="count-selector8"]'
        party_button = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, group_size_2))
        )
        party_button.click()
        print("Party size button clicked.")
    except TimeoutException:
        print("Couldn't click party size")
        driver.quit()
        return False

    # Select the desired date
    day = "2024-06-27"  # NOTE: This can be updated later based on the format of the xpaths to iteratively check different days as desired.
    date_xpath = '/html/body/app-root/div/app-core-layout/div/div[2]/div/app-component-switcher/app-restaurant-details-date-range/div/section[2]/app-search-range-availability-criteria/section[2]/div/div/dpep-date-range-calendar-picker/div/div[1]/dpep-date-range-calendar[1]/div/div[2]/table/tbody/tr[5]/td[5]/div/a'
    try:
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, date_xpath))).click()
    except TimeoutException:
        print("Couldn't select date")
        driver.quit()
        return False

    # Select the Next button
    next_xpath = '//*[@id="btnCancel"]'
    try:
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, next_xpath))).click()
    except TimeoutException:
        print("Couldn't click next")
        driver.quit()
        return False

    # Handle the results
    reservation_not = '/html/body/app-root/div/app-core-layout/div/div[2]/div/app-component-switcher/app-restaurant-details-date-range/div/section[2]/div/div'
    reservation_yes_maybe = '/html/body/app-root/div/app-core-layout/div/app-component-switcher/app-restaurant-details-date-range/div/section[2]/div/div/div'
    try:
        exists = check_xpath_exists(driver, reservation_yes_maybe)
        driver.quit()
        current_time = datetime.fromtimestamp(TIME.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Satus is {exists } at: {current_time}")
        return exists
    except TimeoutException:
        print("No available times found or page took too long to load.")
        driver.quit()
        return False

def attempt_reservation(sc):
    if not make_reservation():
        # Schedule the next attempt in 1 minute
        scheduler.enter(60, 1, attempt_reservation, (sc,))

def main():
    # Initial scheduling
    scheduler.enter(0, 1, attempt_reservation, (scheduler,))
    scheduler.run()

if __name__ == "__main__":
    main()

# Print the current time and date

