# Flower_Shop
Это сайт сети FlowerShop. Здесь можно заказать превосходные букеты с доставкой на дом.

![image](https://github.com/FOURWORDSALLCAPS/Flower_Shop/assets/48273739/315b160f-1f0e-43dd-805a-13e6811e1d34)

## Сайт онлайн

Тут можно проверить сайт в работе: [Flower_Shop](https://www.kek.lolkekazaza.ru/)

## Запуск

- Скачайте код
- Установите зависимости 
- Создайте файл базы данных и сразу примените все миграции командой `python3 manage.py migrate`
- Запустите сервер командой `python3 manage.py runserver`

## Установка зависимостей:

Операционная система Windows
 - Запускаем CMD (можно через Win+R, дальше вводим`cmd`) и вписываем команду`cd /D <путь к папке со скриптами>`

Операционная система Linux
 - Запускаем Terminal (Ctrl + Alt + T) и вписываем команду`cd /D <путь к папке со скриптами>`

Операционная система macOS
 - Запускаем Terminal (Вид>Терминал) и вписываем команду`cd /D <путь к папке со скриптами>`

```pip install -r requirements.txt```

## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` рядом с `manage.py` и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступны 4 переменные:
- `DEBUG` — дебаг-режим. Поставьте True, чтобы увидеть отладочную информацию в случае ошибки.
- `SECRET_KEY` — секретный ключ проекта
- `ALLOWED_HOSTS` — см [документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts).
- `STRIPE_API_KEY` — см [документацию Stripe](https://stripe.com/docs/api).

## Версия Python: 
Мы использовали Python `3.8.3`, но он должен работать на любой более новой версии.

## Цель проекта:
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).

## Авторы
(2023) Zaitsev Vladimir Goncharov Aleksandr
