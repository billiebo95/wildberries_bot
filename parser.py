import requests
from bs4 import BeautifulSoup

def get_price(article):
    try:
        url = f"https://www.wildberries.ru/catalog/{article}/detail.aspx"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, "html.parser")

        price_tag = soup.select_one("ins.price-block__final-price.wallet")
        if price_tag:
            price_text = price_tag.text.strip().replace('\xa0', '').replace('₽', '')
            return int(price_text)

        print("❌ Цена не найдена в HTML")
        return None

    except Exception as e:
        print("❌ Ошибка при парсинге:", e)
        return None
