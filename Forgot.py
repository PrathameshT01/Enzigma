import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Setup the WebDriver
service = Service("C:/WebDriver/chromedriver.exe")
driver = webdriver.Chrome(service=service)


# Helper function to open forgot password page
def open_forgot_password():
    """Navigates to the forgot password page."""
    driver.get("https://app-staging.nokodr.com/super/apps/auth/v1/index.html#/loginu")
    try:
        # Wait for the "Forgot Password?" link and click it
        forgot_password = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Forgot Password?"))
        )
        forgot_password.click()
        print("Forgot Password page opened successfully.")
    except (NoSuchElementException, TimeoutException) as error:
        print(f"Error navigating to Forgot Password page: {error}")


# Function to check the email field for validation
def check_email_field():
    """Checks if the email field exists and verifies if it's required."""
    try:
        # Ensure the email field is present
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_17406477278348063"))
        )
        print("Email field is located.")

        # Check if the field is required
        if email_input.get_attribute('required'):
            print("Email field is mandatory.")
    except (NoSuchElementException, TimeoutException) as error:
        print(f"Error finding the email field: {error}")


# Function to test valid email submission
def submit_valid_email():
    """Tests forgot password functionality with a valid email."""
    try:
        email_input = driver.find_element(By.ID, "id_17406477278348063")
        submit_btn = driver.find_element(By.ID, "staticElement")

        # Input a valid registered email
        email_input.clear()
        email_input.send_keys("registered@example.com")
        submit_btn.click()

        # Wait for the success message
        success_msg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Reset link sent to your email')]"))
        )
        print("Success: ", success_msg.text)
    except (NoSuchElementException, TimeoutException) as error:
        print(f"Error during valid email test: {error}")


# Function to test invalid email scenarios
def submit_invalid_emails():
    """Tests forgot password functionality with invalid emails."""
    try:
        email_input = driver.find_element(By.ID, "id_17406477278348063")
        submit_btn = driver.find_element(By.ID, "staticElement")

        # Test non-registered email
        email_input.clear()
        email_input.send_keys("nonregistered@example.com")
        submit_btn.click()

        # Check error message for non-registered email
        error_msg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Email not found')]"))
        )
        print("Error with non-registered email: ", error_msg.text)

        # Test invalid email format
        email_input.clear()
        email_input.send_keys("invalid-email-format")
        submit_btn.click()

        invalid_email_msg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Invalid email format')]"))
        )
        print("Error with invalid email format: ", invalid_email_msg.text)

        # Test empty email field
        email_input.clear()
        submit_btn.click()

        empty_field_msg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Email is required')]"))
        )
        print("Error with blank email field: ", empty_field_msg.text)

    except (NoSuchElementException, TimeoutException) as error:
        print(f"Error during invalid email tests: {error}")


# Run the tests
open_forgot_password()
check_email_field()
submit_valid_email()
submit_invalid_emails()

# Close the browser after tests
input("Press Enter to close the browser...")
driver.quit()
