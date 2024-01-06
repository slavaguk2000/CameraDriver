import pygame
import serial
import struct
import time

MIN_X_ZERO = -5
MIN_Y_ZERO = 0
MAX_X_ZERO = 0
MAX_Y_ZERO = 0

# Инициализация pygame
pygame.init()

# Инициализация джойстика
pygame.joystick.init()

# Настройки для последовательного порта
serialPort = serial.Serial(port='COM4', baudrate=115200, timeout=1)  # Замените 'COM3' на ваш порт

# Функция для отправки данных через Serial
def send_data(x, y):
    sending_x = x + 5000
    sending_y = y + 5000

    data = struct.pack('>BBBBBBBB', 255, min(int(sending_x / 100), 99), int(sending_x % 100), min(int(sending_y / 100), 99), int(sending_y % 100), 0, 0, 0)
    serialPort.write(data)

def normalize_value(value, min_zero, max_zero):
    return max(value - max_zero, 0) if value > 0 else min(value - min_zero, 0)


try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Основной цикл
    running = True
    while running:
        start_time = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Получение положения осей джойстика
        x = normalize_value(pow(joystick.get_axis(0), 3) * 4999, MIN_X_ZERO, MAX_X_ZERO)  # Умножаем на 32767 для преобразования в int16
        y = normalize_value(pow(joystick.get_axis(1), 3) * (-4999), MIN_Y_ZERO, MAX_Y_ZERO)

        # Отправка данных через Serial
        send_data(x, y)

        # Вывод данных на экран
        print(f"x: {int(x)}, y: {int(y)}")

        # Поддержание частоты отправки в 100 Гц
        time.sleep(max(0, 0.01 - (time.time() - start_time)))

except pygame.error:
    print("Не удалось обнаружить джойстик")

finally:
    pygame.quit()
    # serialPort.close()
