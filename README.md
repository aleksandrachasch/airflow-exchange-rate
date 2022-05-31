# Выгрузка данных по валютной паре BTC/USD в Postgres на Airflow

## Что было сделано
Создано 3 контейнера: Airflow, Postgres и PGAdmin. 

ETL-процесс разбит на три задачи:
1. Создание таблицы `rate`в Postgres (если она уже не создана)
1. Выгрузка данных по валютной паре через API
2. Загрузка данных в таблицу `rate`

## Инструкция по запуску

1. `git clone https://github.com/aleksandrachasch/airflow-exchange-rate.git`
2. `cd airflow-exhange-rate`
3. `docker compose up`

## Инструкция по применению

### Создание соединения с Postgres

1. Открыть в браузере Airflow UI: http://localhost:8080/
2. В меню выбрать `Admin > Connections > Create`
3. Заполнить поля так, как показано на снимке экрана: <img width="1184" alt="Screenshot 2022-05-31 at 23 59 15" src="https://user-images.githubusercontent.com/16349126/171293808-33daa021-3502-49f9-afd2-4822b7bb8106.png">
4. В поле `Password` ввести "airflow"
5. Нажать на `Create`

### Запуск процесса
1. Запустить DAG через Airflow UI

### Валидация процесса
3. Открыть в браузере PGAdmin: http://localhost:15432/browser/# 
4. Для авторизации использовать почту `airflow@example.com` и пароль `postgres` 
5. Проверить содержимое таблицы `rate`  
