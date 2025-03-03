from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Define the path to the ChromeDriver executable
chrome_service = Service("C:/WebDriver/chromedriver.exe")

# Initialize the WebDriver for Chrome
browser = webdriver.Chrome(service=chrome_service)

# Navigate to the desired webpage
browser.get("https://app-staging.nokodr.com/")

# Print the page title to verify the page has loaded
print("Page Title: ", browser.title)

# Close the browser after use
browser.quit()
