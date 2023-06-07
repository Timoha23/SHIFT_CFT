# SHIFT_CFT
## Описание
___
Данный сервис разработан для просмотра текущей зарплаты сотрудника и даты следующего повышения данной зарплаты. Каждый сотрудник может смотреть только свои данные о зарплате. Администратор имеет право посмотреть зарплату каждого сотрудника и изменить данные о ней. 

<i>* - на случайную</i>
<details>
<summary>ТЗ проекта ↓</summary>

Описание задачи

Реализуйте REST-сервис просмотра текущей зарплаты и даты следующего
повышения. Из-за того, что такие данные очень важны и критичны, каждый
сотрудник может видеть только свою сумму. Для обеспечения безопасности, вам
потребуется реализовать метод где по логину и паролю сотрудника будет выдан
секретный токен, который действует в течение определенного времени. Запрос
данных о зарплате должен выдаваться только при предъявлении валидного токена.
Требования к решению
Обязательные технические требования:

● код размещен и доступен в публичном репозитории на GitLab;

● оформлена инструкция по запуску сервиса и взаимодействию с проектом
(Markdown файл с использованием конструкций разметки от GitLab по
необходимости);

● сервис реализован на FastAPI.
Необязательные технические требования (по возрастанию трудоемкости):

● зависимости зафиксированы менеджером зависимостей poetry;

● написаны тесты с использованием pytest;

● реализована возможность собирать и запускать контейнер с сервисом в Docker.
Вы можете выполнить только часть необязательных технических требований.
Задание будет оцениваться комплексно.
Удачи!
</details>

## Используемые технологии
___
![AppVeyor](https://img.shields.io/badge/Python-3.10.6-green)
![AppVeyor](https://img.shields.io/badge/FastAPI-0.96.0-9cf)
![AppVeyor](https://img.shields.io/badge/Alembic-1.11.1-9cf)
![AppVeyor](https://img.shields.io/badge/SQLAlchemy-2.0.15-9cf)
![AppVeyor](https://img.shields.io/badge/pytest-7.3.1-9cf)
![AppVeyor](https://img.shields.io/badge/uvicorn-0.22.0-9cf)


![AppVeyor](https://img.shields.io/badge/Docker-24.0.2-green)
![AppVeyor](https://img.shields.io/badge/docker--compose-1.29.2-9cf)

![AppVeyor](https://img.shields.io/badge/Postgres-15.0-green)

![AppVeyor](https://img.shields.io/badge/Poetry-1.5.1-green)

## Модели
___

![imageup.ru](https://imageup.ru/img68/4370057/my-first-board.jpg)

## Запуск
___
###  Локально

1. Клонируем репозиторий:
   ```bash
   git clone https://github.com/Timoha23/SHIFT_CFT.git
   ```
2. Переходим в директорию с проектом:
    ```bash
    cd app/
    ```
3. Создаем .env файл и заполняем в соответствии с примером (.env.example).

4. Устанавливаем зависимости:
    ```bash
    poetry install
    ```
5. Накатываем миграции:
   ```bash
   alembic upgrade head
   ```
6. Создаем админа:
   ```bash
   python utils/create_admin.py
   ```
   Данные администратора: username: admin, password: admin
7. Запускаем приложение:
   ```bash
   python app/main.py
   ```
###  Докер
1. Клонируем репозиторий:
   ```bash
   git clone https://github.com/Timoha23/SHIFT_CFT.git
   ```

2. Создаем .env файл и заполняем в соответствии с примером (.env.example).
3. Поднимаем контейнеры:
   ```bash
   docker-compose up -d --build
   ```
4. Пользователь-администратор будет создан автоматически. Данные администратора: username: admin, password: admin
## Примеры запросов
___
### Работа с пользователями

1. Создание пользователя
   * Endpoint: **host:port/users/**
   * Method: **POST**
   * Body: 
      ```json
      {
        "username": "username",
        "email": "user@gmail.com",
        "password": "password",
        "first_name": "Иван",
        "last_name": "Иванов"
      }   
      ```
   * Response: 
      ```json
      {
        "id": "fee12d8e-b170-49a4-ac3e-011af8a385af",
        "username": "username",
        "email": "user@gmail.com",
        "first_name": "Иван",
        "last_name": "Иванов",
        "created_date": "2023-06-07T12:14:02.771000",
        "salary": {
            "id": "90fd9e2d-22fd-465e-a6bd-29a7cbc0e198",
            "current_salary": null,
            "increase_date": null,
            "created_date": "2023-06-07T12:14:02.772928"
        }
      }
      ```
   * Postman
     <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][1]][1]
      
     [1]: https://imageup.ru/img227/4370213/shift_create_user.png
     </details>

2. Получение всех пользователей
   * Endpoint: **host:port/users/**
   * Permissions: **Admin only**
   * Method: **GET**
   * Headers:
      ```json
      {
        "Authorization": "Bearer <token>"
      }
      ```
   * Response: 
      ```json
      [
        {
          "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "username": "string",
          "email": "string",
          "first_name": "string",
          "last_name": "string",
          "created_date": "2023-06-07T12:56:36.910Z",
          "salary": {
          "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "current_salary": 0,
          "increase_date": "2023-06-07T12:56:36.910Z",
          "created_date": "2023-06-07T12:56:36.910Z"
          }
        }
      ]
      ```
   * Postman
     <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][2]][2]
      
     [2]: https://imageup.ru/img133/4370215/get_users.png
     
     </details> 

3. Получение токена
   * Endpoint: **host:port/users/token/**
   * Method: **POST**
   * Headers:
      ```json
      {
        "Content-Type": "application/x-www-form-urlencoded"
      }
      ````
   * Body: 
      ```json
      {
        "username": "username",
        "password": "password"
      }   
      ```
   * Response: 
      ```json
      {
        "access_token": "string",
        "token_type": "string"
      }   
      ```
   * Postman 
     <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][3]][3]
      
     [3]: https://imageup.ru/img286/4370218/get_token.png
     </details>
4. Удаление пользователя
   * Endpoint: **host:port/users/{user_id}**
   * Permissions: **Admin only**
   * Method: **DELETE**
   * Headers:
      ```json
      {
        "Authorization": "Bearer <token>"
      }
   * Params:
     * Path 
      ```json
      {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
      }
      ```
   * Postman 
     <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][4]][4]
      
     [4]: https://imageup.ru/img15/4370222/delete_user.png
     </details>

### Работа с зарплатами

1. Получение инофрмации о своей зарплате
   * Endpoint: **host:port/salary/me/**
   * Method: **GET**
   * Headers:
      ```json
      {
        "Authorization": "Bearer <token>"
      }
   * Response: 
      ```json
      {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "current_salary": 0,
        "increase_date": "2023-06-07T13:07:37.750Z",
        "created_date": "2023-06-07T13:07:37.750Z"
      }
      ```
   * Postman 
     <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][5]][5]
      
     [5]: https://imageup.ru/img85/4370224/get_my_salary.png
     </details>
2. Получение инофрмации о зарплате пользователя
   * Endpoint: **host:port/salary/{user_id}/**
   * Method: **GET**
   * Permissions: **Admin only**
   * Headers:
      ```json
      {
        "Authorization": "Bearer <token>"
      }
   * Params:
      * Path 
      ```json
      {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
      }
      ```
   * Response: 
      ```json
      {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "current_salary": 0,
        "increase_date": "2023-06-07T13:07:37.750Z",
        "created_date": "2023-06-07T13:07:37.750Z"
      }
      ```
   * Postman 
     <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][6]][6]
      
     [6]: https://imageup.ru/img208/4370225/get_user_salary.png
     </details> 
3. Изменение инофрмации о зарплате пользователя
   * Endpoint: **host:port/salary/{user_id}/**
   * Method: **PATCH**
   * Permissions: **Admin only**
   * Headers:
      ```json
      {
        "Authorization": "Bearer <token>"
      }
    * Params:
      * Path 
      ```json
      {
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
      }
      ```
    * Body: 
      ```json
      {
        "current_salary": 100000,
        "increase_date": "2023-06-07T13:14:31.350Z"
      } 
      ```
   * Response: 
      ```json
      {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "username": "string",
        "email": "string",
        "first_name": "string",
        "last_name": "string",
        "created_date": "2023-06-07T13:14:31.366Z",
        "salary": {
          "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
          "current_salary": 100000,
          "increase_date": "2023-06-07T13:14:31.350Z",
          "created_date": "2023-06-07T13:14:31.366Z"
        }
      }
      ```
   * Postman 
     <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][7]][7]
      
     [7]: https://imageup.ru/img55/4370227/update_user_salary.png
     </details> 