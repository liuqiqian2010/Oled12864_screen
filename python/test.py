import time
import numpy as np
from PIL import ImageGrab
import serial

# 预计算权重数组（常量）
WEIGHTS = 2 ** np.arange(7, -1, -1)  # [128, 64, 32, 16, 8, 4, 2, 1]


def screenToData():
    # 截屏并直接调整大小和灰度转换
    img = ImageGrab.grab().resize((128, 64)).convert('L')

    # 转换为numpy数组并进行二值化
    img_array = np.array(img)
    bin_array = np.where(img_array > 30, 1, 0).astype(np.uint8)

    # 重组数据并计算字节值
    byte_array = np.dot(bin_array.reshape(8, 8, 128)[:, ::-1, :].reshape(-1, 8), WEIGHTS)
    return byte_array.astype(np.uint8).tobytes()


if __name__ == '__main__':
    PORT = 'COM4'
    print(len(screenToData()))
    with serial.Serial(PORT, 115200) as ser:
        data = screenToData()
        ser.write(data)
        while True:
            time1 = time.time()
            data = screenToData()
            assert ser.read(2)  # 等待同步信号
            ser.write(data)
            print('FPS:', round(1 / (time.time() - time1), 2))
