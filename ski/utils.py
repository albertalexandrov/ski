from collections import defaultdict
from typing import Dict, Text

import httpx

from settings import ORDERS_SERVER_URL


async def get_order(number: Text, passenger_id: Text) -> Dict:
    """Выполняет запрос заказа на некоторый удаленный сервер.

    Args:
        number: номер брони
        passenger_id: фамилия пассажира

    Returns:
        Данные заказа

    """
    async with httpx.AsyncClient(base_url=ORDERS_SERVER_URL, timeout=1) as client:
        r = await client.get('/get', params={'number': number, 'passengerId': passenger_id})
        r.raise_for_status()

    return r.json()


def extract_ski_data(data: Dict) -> Dict:
    """Возвращает из данных все passengerId, все routeId, baggageIds с equipmentType == ski

    Args:
        data: данные заказа

    Returns:
        Все passengerId, все routeId, baggageIds с equipmentType == ski

    """
    raw_result = defaultdict(list)

    for ancillaries_pricing in data['ancillariesPricings']:
        for baggage_pricing in ancillaries_pricing['baggagePricings']:
            passenger_ids = baggage_pricing['passengerIds']
            route_id = baggage_pricing['routeId']
            for baggage in baggage_pricing['baggages']:
                if 'equipmentType' in baggage and baggage['equipmentType'] == 'ski':
                    for passenger_id in passenger_ids:
                        raw_result[(passenger_id, route_id)].append(baggage['id'])

    return {
        'baggageSelections': [{
            'passengerId': key[0],
            'routeId': key[1],
            'baggageIds': baggage_ids,
            'redemption': False
        } for key, baggage_ids in raw_result.items()]
    }


async def update_order_with_ski(ski_data: Dict) -> None:
    """Добавление лыж.

    Args:
        ski_data: извлеченные из данных заказа данные по лыжам

    """
    async with httpx.AsyncClient(base_url=ORDERS_SERVER_URL, timeout=1) as client:
        r = await client.get('/put', data=ski_data)
        r.raise_for_status()
