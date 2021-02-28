from typing import Dict

from fastapi import status, FastAPI, Query
from httpx import HTTPStatusError
from fastapi.responses import JSONResponse

from utils import get_order, extract_ski_data, update_order_with_ski

app = FastAPI(title='Сервис выполнения заявок на провоз лыж')


@app.get('/')
async def process_ski(number: str = Query(..., title='ID брони', regex='^\\w+$'),
                      passenger_id: str = Query(..., title='Фамилия пассажира', alias='passengerId', regex='^\\w+$')):
    """Выполняет заявку на провоз лыж.

    Args:
        number: номер брони
        passenger_id: фамилия пассажира

    """
    try:
        order: Dict = await get_order(number, passenger_id)
    except (HTTPStatusError, Exception):
        # HTTPStatusError - исключения, связанные с проблемами на удаленном сервере (4**, 5**)
        # Exception - иные исключения, напр., отсутствует выход Интернет
        # Логгирование, sentry, etc.
        content = {
            'error': {
                'code': 'cannot.get.order',
                'message': 'Не удалось получить бронь. Пожалуйста, обновите страницу и попробуйте снова.',
            },
            'shoppingCart': None
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)

    ski_data: Dict = extract_ski_data(order)

    try:
        print(await update_order_with_ski(ski_data))
    except (HTTPStatusError, Exception):
        # HTTPStatusError - исключения, связанные с проблемами на удаленном сервере (4xx, 5xx)
        # Exception - иные исключения, напр., отсутствует выход Интернет
        # Логгирование, sentry, etc.
        content = {
            'error': {
                'code': 'conversation.not.found',
                'message': 'Давайте начнем новый поиск и обновим результаты.',
            },
            'shoppingCart': None
        }
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)

    return {
        "shoppingCart": {}
    }
