from dotenv import load_dotenv
from time import sleep
import requests
import telegram
import argparse
import logging
import os



def get_response_from_api(token, timestamp):
    url = 'https://dvmn.org/api/long_polling/'

    headers = {
        'Authorization': f'Token {token}'
    }

    params = {
        'timestamp': timestamp,
    }

    response = requests.get(url, headers=headers, params=params, timeout=120)
    response.raise_for_status()
    return response.json()


def get_telegram_bot(token):
    return telegram.Bot(token=token)


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
    load_dotenv()
    devman_api_token = os.getenv("DEVMAN_API_TOKEN")
    telegram_bot_api_token = os.getenv('TELEGRAM_BOT_API_TOKEN')

    telegram_bot = get_telegram_bot(telegram_bot_api_token)

    timestamp = ''

    while True:
        try:
            api_response = get_response_from_api(devman_api_token, timestamp)
            logger.debug(f"request_query: {api_response['request_query']}")

            if api_response['status'] == 'timeout':
                timestamp = api_response['timestamp_to_request']

            if api_response['status'] == 'found':
                for attempt in api_response['new_attempts']:
                    message_text = generate_message_text(attempt)
                    telegram_bot.send_message(chat_id=chat_id, text=message_text)
                    timestamp = api_response['last_attempt_timestamp']

        except requests.exceptions.ReadTimeout:
            continue

        except requests.exceptions.ConnectionError:
            logger.debug('Нет подключения к интернету.')
            sleep(1)
            continue

        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('chat_id', type=str, help='Telegram chat ID.')
    parser.add_argument('--logger', action='store_true', help='Enable logger')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('logger')
    logger.disabled = not args.logger

    main(args.chat_id)
