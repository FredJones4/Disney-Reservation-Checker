from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time as TIME

TIMEOUT = 20  # Increase timeout
DISNEY_URL = 'https://disneyworld.disney.go.com/dining/polynesian-resort/ohana/'
DISNEY_EMAIL = 'fake.email099887@gmail.com'
DISNEY_PASSWORD = 'password123'

driver = webdriver.Chrome()

def close_overlay():
    try:
        overlay_xpath = '//*[@id="sec-overlay"]'
        WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, overlay_xpath)))
        driver.execute_script("document.getElementById('sec-overlay').style.display = 'none';")
        print("Overlay closed.")
    except TimeoutException:
        print("No overlay found.")
        pass

def make_reservation():
    driver.get("https://disneyworld.disney.go.com/dining/polynesian-resort/ohana/")

    # Add implicit wait
    driver.implicitly_wait(10)

    # Open the calendar
    try:
        calendar_button_xpath = '//*[@id="finderDetailsContainer-90002606;entityType=restaurant"]/div[1]/finder-aag/div/div[2]/div/finder-button/a'
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, calendar_button_xpath))).click()

    except TimeoutException:
        print("Couldn't load calendar button")
        return

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
        return

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
        return
    # Add implicit wait
    TIME.sleep(10)
    # Initial group size
    cur_size = 8  # Starting with group size 8
    desired_month = "August"  # Change to the desired month
    counter = 0
    # TODO: make this a one-shot
    # while cur_size > 1:  # Prevent group size less than 1
    #     cur_group_size = f'//*[@id="count-selector{cur_size}"]'
    #     next_group_size = f'//*[@id="count-selector{cur_size - 1}"]'
    #
    #     if counter > 6 or cur_size < 1:  # Prevent infinite loop
    #         print("Well, group size was having issues. Moving on:")
    #         # return
    #         break
    #
    #     try:
    #         WebDriverWait(driver, TIMEOUT).until(
    #             EC.element_to_be_clickable((By.XPATH, cur_group_size))).click()
    #         print("Clicked date.")
    #         cur_size -= 1  # Decrement group size
    #         counter += 1
    #     except TimeoutException:
    #         print("Couldn't select group size. Trying again")


    try:
        # Group Size Try 2
        TIME.sleep(5)
        # Close any overlays if present
        close_overlay()

        group_size_2 = '//*[@id="count-selector8"]'
        party_button = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, group_size_2))
        )
        party_button.click()
        print("Continue button clicked.")
    except TimeoutException:
        print("Couldn't click party size")
        return


    # Select the desired date
    day = "2024-06-27"  # NOTE: This can be updated later baesd off the format of the xpaths to iteratively check different days as desired.
    date_xpath = '/html/body/app-root/div/app-core-layout/div/div[2]/div/app-component-switcher/app-restaurant-details-date-range/div/section[2]/app-search-range-availability-criteria/section[2]/div/div/dpep-date-range-calendar-picker/div/div[1]/dpep-date-range-calendar[1]/div/div[2]/table/tbody/tr[5]/td[5]/div/a'
    try:
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, date_xpath))).click()
    except TimeoutException:
        print("Couldn't select date")
        return

    # Select the Next button
    next_xpath = '//*[@id="btnCancel"]'
    try:
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, next_xpath))).click()
    except TimeoutException:
        print("Couldn't click next")
        return


    # # Select party size
    # party_size_dropdown_xpath = '//*[@id="partySize-wrapper"]/div[1]'
    # try:
    #     WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, party_size_dropdown_xpath))).click()
    # except TimeoutException:
    #     print("Couldn't open party size dropdown")
    #     return
    #
    # party_size = "4"  # Change to the desired party size
    # party_size_option_xpath = f'//*[@data-value="{party_size}" and @role="option"]'
    # try:
    #     WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, party_size_option_xpath))).click()
    # except TimeoutException:
    #     print("Couldn't select party size")
    #     return
    #
    # # Submit the search
    # search_button_xpath = '//*[@id="dineAvailSearchButton"]'
    # try:
    #     WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, search_button_xpath))).click()
    # except TimeoutException:
    #     print("Couldn't submit search")
    #     return

    # Handle the results
    try:
        available_times = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'availableTime')))
        times = [time.text for time in available_times]
        print(f"Available times: {times}")
    except TimeoutException:
        print("No available times found or page took too long to load.")


make_reservation()
driver.quit()
