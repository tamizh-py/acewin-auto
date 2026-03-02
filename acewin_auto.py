from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import os
import logging
import requests

# ---------- LOGGING ----------
logging.basicConfig(
    filename="run.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------- TELEGRAM FUNCTION ----------
def send_telegram_message(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("Telegram secrets not set")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(url, data=data, timeout=10)
        print("Telegram status:", response.status_code)
        print("Telegram response:", response.text)
    except Exception as e:
        print("Telegram send failed:", e)


driver = None

try:
    logging.info("Script started")

    # ---------- HEADLESS SETUP ----------
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    # ---------- OPEN WEBSITE ----------
    driver.get("https://www.acewin.in/login")

    # ---------- LOGIN ----------
    wait.until(EC.presence_of_element_located((By.ID, "phone")))

    USERNAME = os.getenv("PHONE")
    PASSWORD = os.getenv("PASSWORD")

    if not USERNAME or not PASSWORD:
        raise Exception("PHONE or PASSWORD not set in secrets")

    driver.find_element(By.ID, "phone").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)

    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    driver.execute_script(
        "arguments[0].click();",
        driver.find_element(By.XPATH, "//button[@type='submit']")
    )

    print("Login clicked")
    time.sleep(4)

    # ---------- CLOSE POPUP ----------
    try:
        actions = ActionChains(driver)
        actions.move_by_offset(10, 10).click().perform()
        print("Popup closed")
        time.sleep(2)
    except:
        print("Popup not present")

    # ---------- CLICK FIRST BUTTON ----------
    first_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div/div[1]/div[2]/div/div[2]/a[3]/div')
        )
    )
    driver.execute_script("arguments[0].click();", first_button)
    print("Clicked Hourly spin button")

    time.sleep(3)

    # ---------- CLICK SECOND BUTTON ----------
    second_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="root"]/div/div/div[1]/section[1]/div/div[2]/div/div[17]/div/div/div[2]/button')
        )
    )
    driver.execute_script("arguments[0].click();", second_button)
    print("Clicked second button")

    time.sleep(10)

    # ---------- SUCCESS ----------
    send_telegram_message("✅ Acewin automation completed successfully")
    logging.info("Script completed successfully")

except Exception as e:
    error_msg = f"❌ Acewin automation failed: {e}"
    print(error_msg)
    logging.error(error_msg)
    send_telegram_message(error_msg)

finally:
    if driver:
        driver.quit()
        logging.info("Browser closed")
