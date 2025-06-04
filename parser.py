import requests
import re

def get_price(article):
    try:
        url = f"https://www.wildberries.ru/catalog/{article}/detail.aspx"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Ищем цену в HTML (цена с учётом скидок)
        match = re.search(r'"price":(\d+),', response.text)
        if match:
            price = int(match.group(1)) / 100  # цена в копейках
            return int(price)

        print("❌ Не нашли цену на странице товара")
        return None
    except Exception as e:
        print("❌ Ошибка при парсинге:", e)
        return None
