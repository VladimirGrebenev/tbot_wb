import requests
import json


def get_info_from_wb(artikul: int) -> dict:
    """
    Функция для извлечения информации о продукте из конкретного URL на
    основе заданного артикула.

    Параметры:
    artikul (int): Уникальный идентификатор продукта

    Возвращает:
    dict: Словарь, содержащий информацию о продукте, такую как бренд, название,
     идентификатор, цена, цена со скидкой и количество товара в наличии
    example {'brand': 'Техно', 'name': 'Пена', 'id': 187338113, 'priceU':
    100000, 'salePriceU': 62700, 'stock': 33}
    """

    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={artikul}"
    response = requests.get(url)
    data = response.json()
    if data["data"]["products"]:
        products = data["data"]["products"]
        total_qty = sum(stock["qty"] for size in
                        data["data"]["products"][0]["sizes"]
                        for stock in size["stocks"])
        for p in products:
            result = {
                "brand": p["brand"],
                "name": p["name"],
                "id": p["id"],
                "priceU": int(p["priceU"]/ 100),
                "salePriceU": int(p["salePriceU"]/ 100),
                "stock": total_qty,
            }

        return result
    else:
        return None

