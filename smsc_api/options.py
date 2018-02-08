from datetime import datetime
from enum import Enum
from typing import Tuple


class Options:
    class Time:
        """
        Время отправки SMS-сообщения абоненту
        """

        def __init__(self, timezone: int = None):
            """
            :param timezone: Часовой пояс, в котором задается параметр time. Указывается относительно московского
            времени. Параметр tz может быть как положительным, так и отрицательным. Если tz равен 0,
            то будет использован московский часовой пояс, если же параметр tz не задан, то часовой пояс будет взят из
            настроек Клиента
            """
            self.timezone = {'tz': timezone} if timezone else {}

        def exact(self, exact: datetime):
            """
            DDMMYYhhmm или DD.MM.YY hh:mm
            :param exact: Время в которое нужно отправить сообщение
            :return: dict с опцией времени
            """
            return {'time': exact.strftime('%d%m%y%H%M'), **self.timezone}

        def timeframe(self, timeframe: Tuple[datetime, datetime]):
            """
            h1-h2. Задает диапазон времени в часах. Если текущее время меньше h1, то SMS-сообщение будет отправлено
            абоненту при наступлении времени h1, если текущее время попадает в промежуток от h1 до h2, то сообщение
            будет отправлено немедленно, в другом случае отправка будет выполнена на следующий день при достижении
            времени h1. Данная функция, например, полезна для того, чтобы не допустить получение SMS-сообщений
            абонентами в ночное время
            :param timeframe: Кортеж с двумя datetime задающими начало и конец диапазона
            :return: dict с опцией времени
            """
            h1, h2 = [h.strftime('%d%m%y%H%M') for h in timeframe]
            return {'time': f'{h1}-{h2}', **self.timezone}

        def timestamp(self, timestamp: int):
            """
            0ts, где ts – timestamp, время в секундах, прошедшее с 1 января 1970 года
            :param timestamp: Время отправки сообщения в формате unix timestamp
            :return: dict с опцией времени
            """
            return {'time': f'0{timestamp}', **self.timezone}

        def delay(self, delay: int):
            """
            +m. Задает относительное смещение времени от текущего в минутах
            :param delay: Задержка отправки в минутах
            :return: dict с опцией времени
            """
            return {'time': f'+{delay}', **self.timezone}

    class Translit(Enum):
        """
        Признак того, что сообщение необходимо перевести в транслит.
        0 (по умолчанию) – не переводить в транслит.
        1 – перевести в транслит в виде "translit".
        2 – перевести в транслит в виде "mpaHc/Ium".
        """
        _key = 'translit'
        NO = {_key: 0}
        YES = {_key: 1}
        IMITATE = {_key: 2}

    class CharSet(Enum):
        """
        Кодировка переданного сообщения, если используется отличная от кодировки по умолчанию windows-1251. Варианты:
        utf-8 и koi8-r.
        """
        _key = 'charset'
        WINDOWS = {_key: 'windows-1251'}
        UTF8 = {_key: 'utf-8'}
        KOI8 = {_key: 'koi-8r'}

    class TinyUrl(Enum):
        """
        Автоматически сокращать ссылки в сообщениях. Позволяет заменять ссылки в тексте сообщения на короткие для
        сокращения длины, а также для отслеживания количества переходов.
        0 (по умолчанию) – оставить ссылки в тексте сообщения без изменений.
        1 – сократить ссылки
        """
        _key = 'tinyurl'
        NO = {_key: 0}
        YES = {_key: 1}

    class ResponseFormat(Enum):
        """
        Формат ответа сервера об успешной отправке.
        0 – (по умолчанию) в виде строки (OK - 1 SMS, ID - 1234).
        1 – вернуть ответ в виде чисел: ID и количество SMS через запятую (1234,1), при cost = 2 еще стоимость через
        запятую (1234,1,1.40), при cost = 3 еще новый баланс Клиента (1234,1,1.40,100.50), при cost = 1 стоимость и
        количество SMS через запятую (1.40,1).
        2 – ответ в xml формате.
        3 – ответ в json формате.
        """
        _key = 'fmt'
        TEXT = {_key: 0}
        CSV = {_key: 1}
        XML = {_key: 2}
        JSON = {_key: 3}

    class ResponseShowCost(Enum):
        """
        Признак необходимости получения стоимости рассылки.
        0 (по умолчанию) – обычная отправка.
        1 – получить стоимость рассылки без реальной отправки.
        2 – обычная отправка, но добавить в ответ стоимость выполненной рассылки.
        3 – обычная отправка, но добавить в ответ стоимость и новый баланс Клиента.
        """
        _key = 'cost'
        NO = {_key: 0}
        DRY_RUN = {_key: 1}
        YES = {_key: 2}
        YES_AND_BALANCE = {_key: 3}

    class ResponseShowBadPhones(Enum):
        """
        Признак необходимости добавления в ответ сервера списка ошибочных номеров.
        0 (по умолчанию) – не добавлять список (обычный ответ сервера).
        1 – в ответ добавляется список ошибочных номеров телефонов с соответствующими статусами.
        """
        _key = 'err'
        NO = {_key: 0}
        YES = {_key: 1}

    class ResponseVerbose(Enum):
        """
        Признак необходимости добавления в ответ сервера информации по каждому номеру.
        0 (по умолчанию) – не добавлять список (обычный ответ сервера).
        1 – в ответ добавляется список всех номеров телефонов с соответствующими статусами, значениями mcc и mnc,
        стоимостью, и, в случае ошибочных номеров, кодами ошибок.
        """
        _key = 'op'
        NO = {_key: 0}
        YES = {_key: 1}

    class MessageType(Enum):
        TEXT = {}
        FLASH = {'flash': 1}
        PUSH = {'push': 1}
        HLR = {'hlr': 1}
        PING = {'ping': 1}
