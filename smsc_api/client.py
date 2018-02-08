from typing import List, Union, NamedTuple, Dict

import requests

from smsc_api.options import Options

URL = 'https://smsc.ru/sys/send.php'


class Message(NamedTuple):
    phones: Union[str, List[str]]
    message: str = ''
    id: Union[str, int] = None
    sender: str = None
    time: Dict[str, str] = {}
    type: Options.MessageType = Options.MessageType.TEXT
    translit: Options.Translit = Options.Translit.NO
    charset: Options.CharSet = Options.CharSet.UTF8
    tinyurl: Options.TinyUrl = Options.TinyUrl.NO
    response_format: Options.ResponseFormat = Options.ResponseFormat.JSON
    response_show_cost: Options.ResponseShowCost = Options.ResponseShowCost.YES_AND_BALANCE
    response_show_bad_phones: Options.ResponseShowBadPhones = Options.ResponseShowBadPhones.YES
    response_verbose: Options.ResponseVerbose = Options.ResponseVerbose.YES
    extra_options: Dict[str, str] = {}

    @property
    def options(self):
        dict_options = [self.translit, self.tinyurl, self.response_format, self.response_show_cost,
                        self.response_show_bad_phones, self.response_verbose, self.charset, self.type]
        options = dict([(key, option.value[key]) for option in dict_options for key in option.value if option])
        if self.id:
            options['id'] = self.id
        if self.sender:
            options['sender'] = self.sender
        return {**self.time, **options, **self.extra_options}

    @property
    def payload(self):
        return dict(
            phones=';'.join(self.phones) if isinstance(self.phones, List) else self.phones,
            mes=self.message,
            **self.options
        )


class Client:
    """
    Клиент для взаимодействия с HTTP API smsc.ru
    """

    def __init__(self, login: str, password: str,
                 sender: str = None,
                 translit: Options.Translit = Options.Translit.NO,
                 charset: Options.CharSet = Options.CharSet.UTF8,
                 tinyurl: Options.TinyUrl = Options.TinyUrl.NO,
                 response_format: Options.ResponseFormat = Options.ResponseFormat.JSON,
                 response_show_cost: Options.ResponseShowCost = Options.ResponseShowCost.YES_AND_BALANCE,
                 response_show_bad_phones: Options.ResponseShowBadPhones = Options.ResponseShowBadPhones.YES,
                 response_verbose: Options.ResponseVerbose = Options.ResponseVerbose.YES
                 ):
        """
        :param login: Логин Клиента
        :param password: Пароль Клиента или MD5-хеш пароля в нижнем регистре
        :param sender: Имя отправителя, отображаемое в телефоне получателя. Разрешены английские буквы, цифры,
        пробел и некоторые символы. Длина – 11 символов или 15 цифр. Все имена регистрируются в личном кабинете.
        :param translit: Признак того, что сообщение необходимо перевести в транслит, варианты - не переводить,
        translit, mpaHc/Ium
        :param charset: Кодировка переданного сообщения
        :param tinyurl: Автоматически сокращать ссылки в сообщениях. Позволяет заменять ссылки в тексте сообщения на
        короткие для сокращения длины, а также для отслеживания количества переходов
        :param response_format: Формат ответа сервера об успешной отправке
        :param response_show_cost: Признак необходимости получения стоимости рассылки
        :param response_show_bad_phones: Признак необходимости добавления в ответ сервера списка ошибочных номеров
        :param response_verbose: Признак необходимости добавления в ответ сервера информации по каждому номеру
        """
        self.login = login
        self.password = password
        self.sender = sender
        self.translit = translit
        self.charset = charset
        self.tinyurl = tinyurl
        self.response_format = response_format
        self.response_show_cost = response_show_cost
        self.response_show_bad_phones = response_show_bad_phones
        self.response_verbose = response_verbose

    @property
    def _auth(self):
        return dict(login=self.login, psw=self.password)

    @property
    def _default_options(self):
        dict_options = [self.translit, self.tinyurl, self.response_format, self.response_show_cost,
                        self.response_show_bad_phones, self.response_verbose, self.charset]
        options = dict([(key, option.value[key]) for option in dict_options for key in option.value if option])
        if self.sender:
            options['sender'] = self.sender
        return options

    def _get(self, params):
        return requests.get(URL, {
            **self._auth,
            **self._default_options,
            **params,
        })

    def send(self, messages: Union[Message, List[Message]]):
        if isinstance(messages, Message):
            messages = [messages]

        results = [self._get(message.payload) for message in messages]
        return results

    def send_text(self, phone: str, text: str, id: str, sender: str):
        return self.send(Message(phones=phone, message=text, id=id, sender=sender))