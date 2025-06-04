from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_price(article):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    try:
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        url = f"https://www.wildberries.ru/catalog/{article}/detail.aspx"
        driver.get(url)

        time.sleep(3)  # Дай странице подгрузиться

        price_el = driver.find_element(By.CLASS_NAME, 'price-block__final-price')
        price_text = price_el.text.replace('\xa0', '').replace('₽', '').strip()

        driver.quit()
        return int(price_text)

    except Exception as e:
        print("❌ Ошибка:", e)
        return None
