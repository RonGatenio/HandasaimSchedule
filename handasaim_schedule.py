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


def get_schedule_html(class_id):
    data = get_schedule_json(class_id)

    data = data['items']

    msg = []
    msg.append(f'<b><u>יום {data[0].get("Text")}</u></b>')
    msg.extend(
        f'<b><code>{u.get("Id", "?")} </code>{u.get("Text", "")}</b>\n<code>  </code>{u.get("Description", "")}' 
        for u in data[1:])
    msg.append('😁')

    return '\n\n'.join(msg)


def get_schedule_html_safe(class_id):
    try:
        return get_schedule_html(class_id)
    except ConnectionException as e:
        return e.msg
    except Exception as e:
        return str(e)
