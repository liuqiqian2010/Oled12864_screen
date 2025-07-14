import time
import cv2
import serial.tools.list_ports
from PIL import ImageGrab


def screenToData():
    image = ImageGrab.grab()  # 截取屏幕
    image.save('image.png')

    image = cv2.imread('image.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转换为灰度图

    thresh, image = cv2.threshold(image, 50, 255, cv2.THRESH_BINARY)  # 二值化图像

    # image = cv2.Canny(image, 0, 255)  # 获取边缘

    image = cv2.resize(image, (128, 64))
    cv2.imwrite('image.png', image)

    image_list = image.tolist()
    data_list = []
    for y in range(8):
        for x in range(128):
            data = ''
            for i in range(8):
                data += '0' if image_list[y * 8 + i][x] == 0 else '1'
            data_list.append(chr(int(data, 2)).encode('ISO-8859-1'))  # 不使用utf-8是因为，一个字符可能会被编码为几个bytes

    return data_list


if __name__ == '__main__':
    PORT = 'COM4'
    with serial.Serial(PORT, 115200) as ser:
        while True:
            time1 = time.time()
            data = bytes().join(screenToData())
            ser.write(data)
            while not (com_input := ser.read(2)):
                pass
            time2 = time.time()
            print('\rFPS: ', 1 / (time2 - time1), end='')
