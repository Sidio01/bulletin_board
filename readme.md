# Доска объявлений ![](https://svgur.com/i/YXB.svg)

## Инструкция по запуску:

~~~
git clone https://github.com/Sidio01/bulletin_board.git
cd bulletin_board
docker-compose build --no-cache
docker-compose up
~~~
Запросы следует отправлять на http://127.0.0.1:8000/

---
---

## Методы:

## Метод получения списка объявлений:

***GET api/v1/ads/list/?page=<<page\>>&sorted=price&order=asc***

Выводит список имеющихся объявлений, отсортированный в требуемом порядке. Количество объявлений на странице - 10.

### Параметры строки запроса:

Параметр|Тип|Описание|Обязательный / опциональный
---|---|---|---
page|integer|Номер страницы списка объявлений|Обязательный
sorted|string|Выбор поля для сортировки списка.<br>Доступные варианты: <li>'price' - сортировка по цене;</li><li>'date' - сортировка по дате.</li>По умолчанию - 'price'.|Опциональный
order|string|Выбор порядка сортировки списка.<br>Доступные варианты: <li>'asc' - сортировка по возрастанию;</li><li>'desc' - сортировка по убыванию.</li>По умолчанию - 'asc'.|Опциональный

### Схема ответа:

Код статуса|Ответ
---|---
200|{{Список под номером объявления}: {"id": {номер в БД}, "title": {Название объявления}, "urls_list": {Ссылка на главную фотографию}, "price": {Цена}}}
400 (при передаче иной очередности сортировки)|{'error': 'Order must be \'asc\' or \'desc\''}
400 (при передаче иного поля для сортировки) |{'error': 'Sorted must be \'price\' or \'date\''}
400 (при отстутствии переданного номера страницы)|{'error': 'Enter page'}
400 (при несоблюдении типа переменной при передаче номера страницы)|{'error': 'Page must be integer'}

---
---

## Метод получения конкретного объявления:

***GET api/v1/ads/{ad_id}/***

Выводит информацию по конкретному объявлению.

### Параметры path:

Параметр|Тип|Обязательный / опциональный
---|---|---
ad_id|integer|обязательный

### Параметры строки запроса:

Параметр|Тип|Описание|Обязательный / опциональный
---|---|---|---
fields|string|Выводит дополнительные поля в ответе:<li>description - описание объявления;</li><li>urls_list - все имеющиеся ссылки на фотографии.</li>|Опциональный

### Схема ответа:

Код статуса|Ответ
---|---
200|{"id": {номер в БД}, "title": {Название объявления}, "urls_list": {Ссылка на главную фотографию}, "price": {Цена}}
200 (при fields=true)|{"id": {номер в БД}, "title": {Название объявления}, "description": {Описание объявления}, "urls_list": {Ссылки на все фотографии}, "price": {Цена}}
404|'error': 'Ad doesn\'t exist'

---
---

## Метод создания объявления:

***POST api/v1/ads/***

Создает объявление с переданными параметрами.

### Параметры тела запроса:

Параметр|Тип|Описание|Обязательный / опциональный
---|---|---|---
title|string|Название объявления:<li>минимум: 1 символ;</li><li>максимум: 200 символов.</li>|Обязательный
description|string|Описание объявления:<li>минимум: 1 символ;</li><li>максимум: 1000 символов.</li>|Обязательный
urls_list|string|Список ссылок на фотографии - одной строкой с разделителем ',' между ссылками. Ссылки в формате 'http://{ссылка}':<li>минимум: 1 символ;</li><li>максимум: 1000 символов.</li>Общее количество ссылок - не более 3-х.|Обязательный
price|integer|Цена|Обязательный


### Схема ответа:

Код статуса|Ответ
---|---
201|{'id': {номер созданного объявления}}
400 (при передаче некорректной ссылки)|{"error": "Enter a valid URL."}
400 (при передачи больше 3-х ссылок)|{"error": "Enter 3 or less URL"}
400 (при передаче переменных некорректных типов)|{"error": "{переменная} is not of type {требуемый тип}"}