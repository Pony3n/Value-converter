# Currency Converter API

Это простое API для конвертации валют, построенное на Django и Django REST Framework. В этом проекте используются Swagger для документации, Docker для контейнеризации и Redis для ускорения работы.

## Функциональность

- Конвертация валют с использованием актуальных обменных курсов.
- Кэширование обменных курсов с использованием Redis.
- Автодокументирование API с помощью Swagger.

## Запуск приложения

### Предварительные требования

- Docker
- Docker Compose

### Установка и запуск

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/yourusername/currency-converter.git
    cd currency-converter
    ```

2. Запустите контейнеры:

    ```bash
    docker-compose up --build
    ```

3. Приложение будет доступно по адресу `http://localhost:8000`.

## Использование

### Swagger UI

Swagger UI доступен по адресу `http://localhost:8000/swagger/`. Используйте его для просмотра и тестирования API.

### Примеры API запросов

#### Конвертация валют (GET запрос)

```http
GET /api/convert/?from=USD&to=EUR&value=100