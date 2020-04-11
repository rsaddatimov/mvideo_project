from ioapi.multicam import RemoteMultiCapture
from ioapi.utils import FPSMeter, env
from urllib.parse import quote_plus
from datetime import *
import logging
import cv2

# TOKEN и IP должны быть в переменных окружения
TOKEN = env.str('TOKEN', 'secret-key')
IP = env.str('IP', 'localhost')
LOGGING_FORMAT = '%(asctime)s [%(levelname)s] %(name)s :: %(message)s'
logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT)

# Время начала воспроизведения
START = '22.11.2019 19:00:00'
# Номера каналов (1 ... 32)
CHANNELS = [15]
# Множитель FPS
FPSX = 2
# Количество кадров, которые надо вытащить с потока
number_of_photos = 1000
# Их счетчик
counter = 0

if __name__ == '__main__':
    pos = datetime.strptime(START, '%d.%m.%Y %H:%M:%S')
    url = 'ws://' + IP + '/api?token=' + quote_plus(TOKEN)
    fps = FPSMeter(autodump=1)

    cap = RemoteMultiCapture(url)
    cap.channels = CHANNELS
    cap.fpsx = FPSX
    cap.pos = pos

    while True:
        fps.tick()
        # пробуем считать кадр
        try:
            ret, frames = cap.read()
        except Exception:
            pass
        if not ret: break
        for frame in frames:
            # сохраняем кадр .jpg и создаем соотвествующий ему .txt
            camera = str(CHANNELS[0])
            second = str(counter // 6)
            num_frame = str(counter % 6)
            name = "c" + camera + "_20191122_1900_" + second + "_" + num_frame
            cv2.imwrite(name + ".jpg", frame.image)
            f = open(name + ".txt", 'w')
            f.close()
            counter += 1
            if (counter == number_of_photos):
                break
        if (counter == number_of_photos):
            break
        if cv2.waitKey(1) & 0xFF == ord('q'): break

    del fps  # Удаление объекта завершает поток авто-вывода
