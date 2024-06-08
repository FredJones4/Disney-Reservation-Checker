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
        sign_in_button_xpath = '//*[@id="dssLogin"]/div[2]/button'
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath))).click()


    except TimeoutException:
        print("Couldn't sign in")
        return

    # Navigate to desired month
    next_month_button_xpath = '//*[@id="ui-datepicker-div"]/div/a[2]'
    month_name_xpath = '//*[@id="ui-datepicker-div"]/div/div/span[1]'
    desired_month = "December"  # Change to the desired month
    counter = 0
    while driver.find_element(By.XPATH, month_name_xpath).text.lower() != desired_month.lower():
        if counter > 6:  # Prevent infinite loop
            break
        try:
            WebDriverWait(driver, TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, next_month_button_xpath))).click()
        except TimeoutException:
            print("Couldn't click next on calendar")
            return
        counter += 1

    # Select the desired date
    day = "25"  # Change to the desired day
    date_xpath = f'//*[@id="ui-datepicker-div"]/table/tbody/tr//a[text()={day}]'
    try:
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, date_xpath))).click()
    except TimeoutException:
        print("Couldn't select date")
        return

    # Select the time
    time_dropdown_xpath = '//*[@id="searchTime-wrapper"]/div[1]'
    try:
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, time_dropdown_xpath))).click()
    except TimeoutException:
        print("Couldn't open time dropdown")
        return

    reservation_time = "6:00 PM"  # Change to desired time
    time_option_xpath = f'//*[@data-display="{reservation_time}"]'
    try:
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, time_option_xpath))).click()
    except TimeoutException:
        print("Couldn't select time")
        return

    # Select party size
    party_size_dropdown_xpath = '//*[@id="partySize-wrapper"]/div[1]'
    try:
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, party_size_dropdown_xpath))).click()
    except TimeoutException:
        print("Couldn't open party size dropdown")
        return

    party_size = "4"  # Change to the desired party size
    party_size_option_xpath = f'//*[@data-value="{party_size}" and @role="option"]'
    try:
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, party_size_option_xpath))).click()
    except TimeoutException:
        print("Couldn't select party size")
        return

    # Submit the search
    search_button_xpath = '//*[@id="dineAvailSearchButton"]'
    try:
        WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, search_button_xpath))).click()
    except TimeoutException:
        print("Couldn't submit search")
        return

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
