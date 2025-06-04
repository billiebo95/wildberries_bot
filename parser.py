import requests

def get_price(article):
    try:
        url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&nm={article}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        products = data.get("data", {}).get("products", [])
        if not products:
            print("❌ Товар не найден в ответе от WB API")
            return None

        price = products[0].get("priceU")
        if price:
            return int(price / 100)
        else:
            print("❌ Цена не найдена")
            return None
    except Exception as e:
        print("❌ Ошибка при получении цены:", e)
        return None
