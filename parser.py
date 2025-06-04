from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def get_price(article):
    url = f"https://www.wildberries.ru/catalog/{article}/detail.aspx"

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(url)
        time.sleep(3)
        price_element = driver.find_element("xpath", '//span[@class="price-block__final-price"]')
        price_text = price_element.text.replace('₽', '').replace(' ', '').replace('\u2009', '')
        return int(price_text)
    except Exception as e:
        print("Ошибка при парсинге:", e)
        return None
    finally:
        driver.quit()
