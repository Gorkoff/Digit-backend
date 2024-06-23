import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

def get_data_impact_factor(data):
    # Удаление ненужных колонок
    exchange_rate_csv = data.drop(columns=['id', 'url', 'title', 'text', 'cluster_id'])

    # Установка индекса и преобразование дат
    exchange_rate_csv.set_index('published_dt', inplace=True)
    data['published_dt'] = pd.to_datetime(data['published_dt'])

    # Группировка данных по времени и идентификатору кластера
    cluster_time_series = data.groupby(['published_dt', 'cluster_id']).size().unstack(fill_value=0)

    # Установка индекса и преобразование дат
    exchange_rate_csv.index = pd.to_datetime(exchange_rate_csv.index)
    cluster_time_series.index = pd.to_datetime(cluster_time_series.index)

    # Объединение данных
    combined_data = exchange_rate_csv.join(cluster_time_series, how='inner')

    # Обработка NaN значений
    combined_data = combined_data.dropna()

    # Разделение данных на обучающую и тестовую выборки
    train_size = int(len(combined_data) * 0.8)
    train, test = combined_data[:train_size], combined_data[train_size:]

    # Параметры модели ARIMA
    p = 1
    d = 1
    q = 1

    # Создание и обучение модели ARIMA
    model = ARIMA(train['currency_curs'], exog=train.drop(columns=['currency_curs']), order=(p, d, q))
    model_fit = model.fit()

    # Прогнозирование на тестовой выборке
    predictions = model_fit.predict(start=len(train), end=len(combined_data) - 1,
                                    exog=test.drop(columns=['currency_curs']), dynamic=False)

    # Получение коэффициентов модели
    coefficients = model_fit.params

    # Преобразование ключей словаря в строки
    coef_dict = {}
    for k, v in coefficients.items():
        if isinstance(k, str) and '.' in k:
            key = k.split('.')[1]
        else:
            key = str(k)
        coef_dict[key] = v

    # Функция для присвоения коэффициентов
    def get_impact_factor(cluster_id):
        return coef_dict.get(str(cluster_id), 0)

    # Присвоение коэффициентов
    data['impact_factor'] = data['cluster_id'].apply(get_impact_factor).round(2)

    return data
