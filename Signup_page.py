from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


class WebDriverContext:
    def __init__(self, service_path):
        self.service = Service(service_path)

    def __enter__(self):
        self.driver = webdriver.Chrome(service=self.service)
        return self.driver

    def __exit__(self, exc_type, exc_value, traceback):
        input("Press Enter to close the browser...")
        self.driver.quit()


def validate_mandatory_fields(driver):
    try:
        driver.get("https://app-staging.nokodr.com/super/apps/auth/v1/index.html#/login")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "signup_button_id"))).click()

        name_field = driver.find_element(By.ID, "id_1740589192196393")
        email_field = driver.find_element(By.ID, "id_17405890626872154")
        password_field = driver.find_element(By.ID, "id_17405891922005504")
        confirm_password_field = driver.find_element(By.ID, "id_17405891922005504-confirmpassword")

        name_field.send_keys("Test User")
        email_field.send_keys("testuser@example.com")
        password_field.send_keys("ValidPassword123")
        confirm_password_field.send_keys("ValidPassword123")

        time.sleep(5)
        success_message = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Account created successfully!')]"))
        )
        print("Signup successful:", success_message.text)

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error occurred: {e}")


def test_invalid_email_format(driver):
    try:
        driver.get("https://app-staging.nokodr.com/super/apps/auth/v1/index.html#/login")
        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
        email_field.send_keys("invalid-email-format")

        driver.find_element(By.ID, "id_17405891922005504").send_keys("ValidPassword123")
        driver.find_element(By.ID, "id_17405891922005504-confirmpassword").send_keys("ValidPassword123")
        driver.find_element(By.ID, "signup_button_id").click()

        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Invalid email format')]"))
        )
        print("Invalid email format detected:", error_message.text)

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error occurred: {e}")


def test_password_mismatch(driver):
    try:
        driver.get("https://app-staging.nokodr.com/super/apps/auth/v1/index.html#/login")
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "id_17405891922005504")))
        confirm_password_field = driver.find_element(By.ID, "id_17405891922005504-confirmpassword")

        password_field.send_keys("ValidPassword123")
        confirm_password_field.send_keys("DifferentPassword456")
        driver.find_element(By.ID, "signup_button_id").click()

        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Passwords do not match')]"))
        )
        print("Password mismatch detected:", error_message.text)

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error occurred: {e}")


if __name__ == "__main__":
    with WebDriverContext("C:/WebDriver/chromedriver.exe") as driver:
        validate_mandatory_fields(driver)
        test_invalid_email_format(driver)
        test_password_mismatch(driver)
