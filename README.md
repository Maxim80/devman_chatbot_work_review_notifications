# Отправляем уведомления о проверке работ
Telegram чат-бот который отправляет уведомления о проверенных работах выполненных в рамках курса по python-программированию на сайте [Devman](https://dvmn.org/).
![](./devman-bot.gif)
  
  
## Как установить
```
git clone https://github.com/Maxim80/devman_chatbot_work_review_notifications.git
cd devman_chatbot_work_review_notifications/
pip install -r requirements.txt
```
  
  
## Как запустить
Перед запуском необходимо добавить следующие переменные окружения:  
`export DEVMAN_API_TOKEN=<значение>` API токен devman.  
`export TELEGRAM_BOT_API_TOKEN=<значение>` telegram bot токен.  
`export ADMIN_CHAT_ID=<значение>` ID чата администратора, куда будут присылаться логи.  
`export USER_CHAT_ID=<значение>` ID чата пользователя, куда будет присылаться информация о проверенных работах.  
    
  
Запустить:
```
python main.py <ваш telegram chat ID> --logger
```
Аргументы:  
`chat_id` - Обязательный агрумент, ваш telegram chat id.  
`--logger` - Не обязательный аргумент, включает debug.  
  
  
## Цели проекта
Проект написан в учебных целях в рамках курса по python-программированию на сайте [Devman](https://dvmn.org/).
