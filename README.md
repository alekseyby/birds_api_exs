# Тестовое задание

Использовал Python 3.6. Для запуска кода скачайте репозиторий
```
git clone https://github.com/alekseyby/birds_api_exs
```
Установите библиотеки
```
$ pip install -r requirements.txt
```

Создаем базу в postgres, и заполняем данными из second_task_init.sql 
```
su postgres -c psql

CREATE USER ornitologist WITH PASSWORD 'ornitologist';
CREATE DATABASE birds_db;
GRANT ALL PRIVILEGES ON DATABASE birds_db TO ornitologist;

BEGIN;
\i second_task_init.sql
COMMIT;
```

# 1-я задача

Решение в файле task1.sql 
```
CREATE TABLE bird_colors_info as SELECT color, COUNT(*)
    FROM birds
    GROUP BY color;
```

#  2-я задача
не выполнена

# 3-я задача
запуск программы:

```
python app.py run

```
запустить юнит-тесты:
```
$ pytest test_birds_api.py
```

