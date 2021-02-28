from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient
from httpx import HTTPStatusError

from ski.main import app
from ski.utils import extract_ski_data

client = TestClient(app)


class TestOrder:

    def test_bad_query_params(self):
        """Тестирование обработки некорректных параметров запроса (query params).

        Notes:
            Параметры number и passengerId обязательные.

        """
        response = client.get('/')
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        response = client.get('/', params={'number': 'AAAAAA'})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        response = client.get('/', params={'passengerId': 'ivanov'})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_getting_order_failed(self):
        """Тестирование случая, когда во время попытки получить инфо по заказу
        был получен ответ со статусом 4хх, 5хх."""

        with patch('ski.main.get_order', side_effect=HTTPStatusError):
            response = client.get('/', params={'number': 'AAAAAA', 'passengerId': 'ivanov'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_updating_order_failed(self, order):
        """Тестирование случая, когда во время попытки обновления заказа
        удаленный сервер вернул ответ со статусом 4хх, 5хх."""

        with patch('ski.main.get_order', return_value=order), \
             patch('ski.main.update_order_with_ski', side_effect=HTTPStatusError):
            response = client.get('/', params={'number': 'AAAAAA', 'passengerId': 'ivanov'})
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_success(self, order):
        """Тестирование успешного выполнения заявки на добавление лыж."""

        with patch('ski.main.get_order', return_value=order), \
             patch('ski.main.update_order_with_ski', return_value=None):
            response = client.get('/', params={'number': 'AAAAAA', 'passengerId': 'ivanov'})
        assert response.status_code == status.HTTP_200_OK


def test_extract_ski(order, extracted_from_order):
    """Тестирование извлечения данных passengerId, routeId,
    baggageIds с equipmentType == ski из данных заказа."""

    fact_result = extract_ski_data(order)
    for res in fact_result, extracted_from_order:
        res['baggageSelections'].sort(key=lambda item: item['passengerId'])
    assert fact_result == extracted_from_order
