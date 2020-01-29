from ioapi.multicam.base import Frame, BaseMultiCapture
from datetime import *
import numpy as np
import websocket
import logging
import json
import cv2

# Пока что логирование не нужно
#logger = logging.getLogger(__name__)


class RemoteMultiCapture(BaseMultiCapture):
    """
    Клиент-серверная имплементация BaseMultiCapture
    -----------------------------------------------
    Проксирующая "обертка" над объектом ThreadedMultiCapture,
    который живет на удаленном сервере.
    Параметры конструктора:
    - url (str) - ссылка для подключения к удаленному серверу
    в формате ws://<host>/api?token=<token>
    """

    def __init__(self, url: str):
        """
        Клиент-серверная имплементация BaseMultiCapture
        :param url: ссылка для подключения к удаленному серверу
        """
        super().__init__()
        self.sock = websocket.WebSocket()
        self.sock.connect(url, timeout=3)

    def __del__(self):
        # При удалении объекта закрываем сокет
        if self.sock.connected:
            self.sock.close(timeout=0.1)

    def _prop_set(self, name, value):
        """
        Устанавливает свойству <name> значение <value> на удаленном сервере
        """
        if isinstance(value, datetime):
            # datetime -> str
            value = value.isoformat()
        # Пакуем в JSON
        msg = json.dumps({
            'event': 'prop-set',
            'data': {'prop': name, 'value': value},
        })
        self.sock.send(msg)
        msg = json.loads(self.sock.recv())
        if msg['event'] == 'error':
            # Сервер вернул ошибку

            #logger.error(msg['data'])
            raise RuntimeError('Server-side exception (see above)')

    # Проксирующие геттеры-сеттеры (ничего интересного)
    # =================================================

    def set_pos(self, pos):
        self._prop_set('pos', pos)
        super().set_pos(pos)

    def set_end(self, end):
        self._prop_set('end', end)
        super().set_end(end)

    def set_fpsx(self, fpsx):
        self._prop_set('fpsx', fpsx)
        super().set_fpsx(fpsx)

    def set_channels(self, channels):
        self._prop_set('channels', list(channels))
        super().set_channels(channels)

    # =================================================

    def read(self):
        # Отправляем событие на считывание кадра
        self.sock.send(json.dumps({'event': 'read'}))

        # Принимаем словарь с мета-информацией
        msg = json.loads(self.sock.recv())
        if msg['event'] == 'error':
            # Что-то пошло не так

            #logger.error(msg['data'])
            raise RuntimeError('Server-side exception (see above)')
        elif msg['event'] == 'stop':
            # Кадры кончились
            return False, None

        # Обновляем текущую позицию
        self._pos = datetime.fromisoformat(msg['pos'])

        frames = []
        for frame in msg['data']:
            # Принимаем кадр
            raw = self.sock.recv()
            if isinstance(raw, str):
                # Вернулась строка - значит что-то не так.
                # С большой вероятностью этот код вообще никогда не
                # должен вызываться, но на всякий случай надо обработать.
                raise RuntimeError('Unexpected message: %s' % msg)

            # bytes -> массив np.uint8
            buffer = np.frombuffer(raw, dtype=np.uint8)
            # Заворачиваем все что есть в namedtuple
            frames.append(Frame(
                channel=frame['channel'],
                time=datetime.fromisoformat(frame['time']),
                image=cv2.imdecode(buffer, cv2.IMREAD_UNCHANGED),
                meta=frame['meta'],
            ))

        return True, tuple(frames)