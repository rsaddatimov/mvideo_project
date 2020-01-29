from frozendict import frozendict
from datetime import *
import numpy as np


class Frame:
    """
    Неизменяемая обертка с информацией о кадре
    ------------------------------------------
    Поля и свойства:
    - channel (int) - номер канала
    - time (datetime) - время кадра
    - image (np.ndarray) - изображение
    - meta (dict) - дополнительная информация
    - size (int, int) - размер изображения (width, height)
    """

    def __init__(self, channel: int = None, time: datetime = None,
                 image: np.ndarray = None, meta: dict = None):
        if channel is None:
            raise ValueError('Required argument: channel')

        if time is None:
            raise ValueError('Required argument: time')

        if image is None:
            raise ValueError('Required argument: image')

        self._channel = channel
        self._time = time
        self._image = image
        self._meta = frozendict(meta or {})

        # Запрещаем прямые изменения изображения
        self._image.setflags(write=False)

    def __repr__(self):
        return (
            f'Frame(channel={self.channel}, '
            f'time={self.time}, '
            f'size={self.size})'
        )

    # Публичные атрибуты (readonly)
    channel = property(lambda self: self._channel)
    time = property(lambda self: self._time)
    image = property(lambda self: self._image)
    meta = property(lambda self: self._meta)
    size = property(lambda self: self._image.shape[1::-1])

    def update_meta(self, **overrides):
        """
        Клонирует объект, обновляя атрибут meta переданными значениями
        """
        meta = self._meta.copy(**overrides)
        return self.copy(meta=meta)

    def copy(self, **overrides):
        """
        Клонирует объект, перезаписывая атрибуты, переданные в overrides
        """
        kwargs = dict(
            channel=self._channel,
            time=self._time,
            image=self._image,
            meta=self._meta,
        )
        kwargs.update(overrides)
        return Frame(**kwargs)
