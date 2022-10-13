# Перед запуском

Створити .env файл з наступними змінними:
```
BOT_TOKEN=токен бота
ADMINS=ID адміністраторів через кому

WEBHOOK_URL=URL для вебхуків
WEBHOOK_HOST=Хост на якому буде підніматись сервер
WEBHOOK_PORT=Порт на якому буде підніматись сервер

FIREBASE_CERTIFICATE_PATH=шлях до сертифікату для firebase(Я скину його Максиму)

DB_USER=exampleDBUserName
PG_PASSWORD=examplePostgresPass
DB_PASS=exampleDBPassword
DB_NAME=exampleDBName
DB_HOST=db

```
# Запуск

Для запуску треба завантажити docker

```sudo apt install docker```

Замість ```apt``` пакетний менеджер вашої системи

Потім виконати команду

```docker-compose start```

і бот запуститься

P.S. Якщо юзаєте nginx то в             ```docker-compose.yml``` є налаштування для nginx(можливо треба буде там шось підправити)