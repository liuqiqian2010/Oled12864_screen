import time
import numpy as np
from PIL import ImageGrab
import serial


WEIGHTS = 2 ** np.arange(7, -1, -1)
def screenToData():
    # 截屏并直接调整大小和灰度转换
    img = ImageGrab.grab().resize((128, 64)).convert('L')

    img = np.array(img)
    img = np.where(img > 30, 1, 0).astype(np.uint8)  # 二值化图像
    img = np.transpose(img)
    img = np.reshape(img, (128, 8, 8))
    img = np.transpose(img, (1, 0, 2))
    img = np.reshape(img, (1024, 8))

    img = np.flip(img, axis=1)
    img = np.dot(img, WEIGHTS)

    # for i in img.tolist():
    #     data.append(chr(int(''.join(i)[::-1], 2)).encode('ISO-8859-1'))

    return img.astype(np.uint8).tobytes()


if __name__ == '__main__':
    PORT = 'COM4'
    with serial.Serial(PORT, 115200) as ser:
        data = screenToData()
        ser.write(data)
        while True:
            time_0 = time.time()
            data = screenToData()
            # time_1 = time.time()
            assert ser.read(2)  # 等待同步信号
            # time_2 = time.time()
            ser.write(data)
            time_3 = time.time()
            print('FPS:', round(1 / (time_3 - time_0), 2))
            # print('处理图片耗时:', time_1 - time_0)
            # print('等待耗时:', time_2 - time_1)
            # print('传输耗时:', time_3 - time_2)
            print('\033[2A')
