# Боты

Данный проект включает двух ботов, в [Телегаме](https://t.me/verbs_game_123_bot) и в [ВКонтакте](https://vk.com/al_im.php?sel=-225996488)

Боты используют Dailogflow и демонстрируют базовый принцип работы - будут реагировать на простые сообщения.

Пример работы телеграм бота:

![Пример работы телеграм бота](https://i.postimg.cc/7L1pHYSN/telegram-gif.gif)


Пример работы ВКонтакте бота:

![Пример работы ВКонтакте бота](https://i.postimg.cc/90wbfJvj/vk-gif.gif)

# Установка и запуск
Для установки нужно скопировать файлы

Затем использовать
```
pip install -r requirements.txt
```

Создать файл `.env`, прописать следующие переменные окружения:
```
TELEGRAM_TOKEN= токен бота в Телеграме
PROJECT_ID= название проекта в google dialogflow
VK_KEY= токен бота ВКонтакте
```

Для запуска Телеграм бота:

```
python telegram_bot.py
```


Для запуска бота ВКонтакте:

```
python vk_bot.py
```
