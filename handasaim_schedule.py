from contextlib import contextmanager
import requests


URL = 'http://ysbhost.com:5001/sc'


TIME_TABLE = {
    0: '7:45 - 8:30',
    1: '8:30 - 9:15',
    2: '9:15 - 10:00',
    3: '10:15 - 11:00',
    4: '11:00 - 11:45',
    5: '12:10 - 12:55',
    6: '12:55 - 13:40',
    7: '13:50 - 14:35',
    8: '14:35 - 15:20',
    9: '15:25 - 16:10',
    10: '16:10 - 16:55',
    11: '17:00 - 17:45',
}


class ConnectionException(Exception):
    def __init__(self, request_response):
        msg = '{} request to "{}" failed with <{}|{}>\n{}'.format(
            request_response.request.method,
            request_response.url,
            request_response.status_code,
            request_response.reason,
            request_response.json()
        )
        super().__init__(msg)
        self.msg = msg


def get_schedule_json(class_id):
    res = requests.post(URL, data={'class': class_id})
    if res.status_code != 200:
        raise ConnectionException(res)
    return res.json()


def _entry_to_str(e):
    id = e.get("Id", "?")
    space_len = len(str(id)) + 1
    time_str = f'<b><i>{TIME_TABLE[id]}</i></b>\n' if id in TIME_TABLE else ""
    return f'\u200f{time_str}<b><code>{e.get("Id", "?"):<{space_len}}</code>{e.get("Text", "")}</b>\n<code>{"":{space_len}}</code>{e.get("Description", "")}'


def get_schedule_html(class_id):
    data = get_schedule_json(class_id)

    data = data['items']

    msg = []
    msg.append(f'<b><u>יום {data[0].get("Text")}</u></b>')
    msg.extend(_entry_to_str(e) for e in data[1:])
    msg.append('😁')

    return '\n\n'.join(msg)


def get_schedule_html_safe(class_id):
    try:
        return get_schedule_html(class_id)
    except ConnectionException as e:
        return e.msg
    except Exception as e:
        return str(e)
