from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import os
import logging

logging.basicConfig(
    filename="run.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

# Configure headless Chrome
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Open browser
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# Open website
driver.get("https://www.acewin.in/login")

# -------- LOGIN SECTION --------
wait.until(EC.presence_of_element_located((By.ID, "phone")))

USERNAME = os.getenv("PHONE")
PASSWORD = os.getenv("PASSWORD")

driver.find_element(By.ID, "phone").send_keys(USERNAME)
driver.find_element(By.ID, "password").send_keys(PASSWORD)
# Click login using fresh locate + JS
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
driver.execute_script(
    "arguments[0].click();",
    driver.find_element(By.XPATH, "//button[@type='submit']")
)

print("Login clicked")

# Wait for page load
time.sleep(4)

# -------- CLOSE POPUP BY CLICKING OVERLAY --------
try:
    actions = ActionChains(driver)
    actions.move_by_offset(10, 10).click().perform()
    print("Popup closed")
    time.sleep(2)
except:
    print("Popup not present")

# -------- CLICK FIRST BUTTON --------
first_button = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/a[3]/div')
    )
)

driver.execute_script("arguments[0].click();", first_button)
print("Clicked Hourly spin button")

time.sleep(3)

# -------- CLICK SECOND BUTTON --------
second_button = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="root"]/div/div/div[1]/section[1]/div/div[2]/div/div[17]/div/div/div[2]/button')
    )
)

driver.execute_script("arguments[0].click();", second_button)
print("Clicked second button")

time.sleep(15)

driver.quit()


