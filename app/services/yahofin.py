from yahoofinancials import YahooFinancials


def get_currency_history(currency='USDRUB=X', start_date="2021-08-01", end_date="2023-08-02"):
    """
    Извлекает исторические данные об открытой цене для указанных валют с Yahoo Finance.

    :param currency: Список валютных пар в формате 'XXXYYY=X'.
    :param start_date: Начальная дата периода (ГГГГ-ММ-ДД).
    :param end_date: Конечная дата периода (ГГГГ-ММ-ДД).
    :return: Словарь с датой(timestamp) и ценой закрытия для каждой валюты.
    """

    yahoo_financials = YahooFinancials(currency)
    historical_data = {}
    price_data = yahoo_financials.get_historical_price_data(start_date, end_date, "daily").get(currency, {}).get(
        'prices', [])
    for data_point in price_data:
        historical_data[f"{data_point['date']}"] = data_point['close']
    return historical_data
