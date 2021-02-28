from configparser import get_configs

configs = get_configs()

ORDERS_SERVER_URL = configs['ordersServerUrl']
