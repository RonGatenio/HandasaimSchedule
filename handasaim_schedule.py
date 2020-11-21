from contextlib import contextmanager
import requests


URL = 'http://ysbhost.com:5001/sc'


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
    id = str(e.get("Id", "?"))
    space_len = len(id) + 1
    return f'<b><code>{e.get("Id", "?"):<{space_len}}</code>{e.get("Text", "")}</b>\n<code>{"":{space_len}}</code>{e.get("Description", "")}'


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
