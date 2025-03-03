import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the WebDriver
service = Service('C:/WebDriver/chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Open the login page of NoKodr platform
driver.get('https://app-staging.nokodr.com/super/apps/auth/v1/index.html#/loginu')

# Set up an explicit wait for elements to load (1800 seconds timeout)
wait = WebDriverWait(driver, 1800)

# Function to check mandatory field validation
def validate_mandatory_fields():
    username = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029323291')))
    password = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029341961')))

    # Ensure both fields are empty
    assert username.get_attribute('value') == '', "Username is not empty"
    assert password.get_attribute('value') == '', "Password is not empty"

    # Try submitting without any input
    login_btn = wait.until(EC.element_to_be_clickable((By.ID, 'staticElement')))
    login_btn.click()

    # Validate that an error message appears
    error = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
    assert 'required' in error.text.lower()

# Function to test valid credentials
def test_login_with_valid_credentials():
    username = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029323291')))
    password = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029341961')))
    login_btn = wait.until(EC.element_to_be_clickable((By.ID, 'staticElement')))

    username.clear()
    password.clear()

    username.send_keys('validUsername')
    password.send_keys('ValidPassword123!')
    login_btn.click()

    # Wait for the redirect to dashboard
    time.sleep(2)
    assert driver.current_url == 'https://app-staging.nokodr.com/super/apps/user-profile/v1/index.html#/', "Login failed"

# Function to test invalid credentials
def test_login_with_invalid_credentials():
    username = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029323291')))
    password = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029341961')))
    login_btn = wait.until(EC.element_to_be_clickable((By.ID, 'staticElement')))

    # Test with wrong username
    username.clear()
    password.clear()
    username.send_keys('invalidUsername')
    password.send_keys('ValidPassword123!')
    login_btn.click()

    error = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
    assert 'Invalid username or password' in error.text

    # Test with wrong password
    username.clear()
    password.clear()
    username.send_keys('validUsername')
    password.send_keys('wrongPassword')
    login_btn.click()

    error = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
    assert 'Invalid username or password' in error.text

# Function to check behavior with blank fields
def test_blank_fields():
    username = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029323291')))
    password = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029341961')))
    login_btn = wait.until(EC.element_to_be_clickable((By.ID, 'staticElement')))

    # Test with blank username
    username.clear()
    password.clear()
    password.send_keys('ValidPassword123!')
    login_btn.click()

    error = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
    assert 'This field is required' in error.text

    # Test with blank password
    username.clear()
    username.send_keys('validUsername')
    password.clear()
    login_btn.click()

    error = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
    assert 'This field is required' in error.text

# Function to test special characters in password
def test_special_characters():
    username = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029323291')))
    password = wait.until(EC.presence_of_element_located((By.ID, 'id_17405881029341961')))
    login_btn = wait.until(EC.element_to_be_clickable((By.ID, 'staticElement')))

    username.clear()
    password.clear()
    username.send_keys('validUsername')
    password.send_keys('Pass@#$%^&*!')
    login_btn.click()

    error = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
    assert 'Invalid username or password' in error.text

# Execute all tests
try:
    validate_mandatory_fields()
    test_login_with_valid_credentials()
    test_login_with_invalid_credentials()
    test_blank_fields()
    test_special_characters()

    input("Press Enter to close the browser...")
finally:
    driver.quit()
