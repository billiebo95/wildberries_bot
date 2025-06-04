
import requests

def get_price(article):
    try:
        url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&nm={article}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        product = data["data"]["products"][0]
        price = product.get("priceU")

        if price:
            return int(price / 100)  # цена в копейках, делим на 100
        return None
    except Exception as e:
        print("Ошибка при получении цены:", e)
        return None
