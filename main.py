from dotenv import load_dotenv
from time import sleep
import requests
import telegram
import argparse
import logging
import os


load_dotenv()


def generate_message_text(attempt):
    title = f'У вас проверили работу "{attempt["lesson_title"]}"\n\n'
    lesson_url = attempt['lesson_url']
    if attempt['is_negative']:
        main_text = 'К сожалению в работе нашлись ошибки.\n\n'
        return f'{title}{main_text}{lesson_url}'
    else:
        main_text = 'Преподавателю все понравилось, можно приступать к следующему уроку!\n\n'
        return f'{title}{main_text}{lesson_url}'


def main(chat_id):
    url = 'https://dvmn.org/api/long_polling/'

    headers = {
        'Authorization': f'Token {os.getenv("DEVMAN_TOKEN")}'
    }

    params = {
        'timestamp': '',
    }

    bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_API_TOKEN'))

    while True:
        try:
            response = requests.get(url, headers=headers, params=params, timeout=120)
            response.raise_for_status()
            response_dict = response.json()
            logger.debug(f"request_query: {response_dict['request_query']}")

            if response_dict['status'] == 'timeout':
                timestamp = response.json()['timestamp_to_request']
                params['timestamp'] = response_dict['timestamp_to_request']

            if response_dict['status'] == 'found':
                for attempt in response_dict['new_attempts']:
                    message_text = generate_message_text(attempt)
                    bot.send_message(chat_id=chat_id, text=message_text)
                    params['timestamp'] = response_dict['last_attempt_timestamp']

        except requests.exceptions.ReadTimeout:
            logger.debug('Нет ответа от сервера.')
            sleep(1)
            continue

        except requests.exceptions.ConnectionError:
            logger.debug('Нет подключения к интернету.')
            sleep(1)
            continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('chat_id', type=str, help='Telegram chat ID.')
    parser.add_argument('--logger', action='store_true', help='Enable logger')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('logger')
    logger.disabled = not args.logger

    try:
        main(args.chat_id)
    except KeyboardInterrupt:
        pass
