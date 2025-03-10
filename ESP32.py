import machine
import ssd1306
import time
import dht

# 初始化 I2C 與 OLED 顯示器
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(110, 32, i2c, addr=0x3C)

# 設定 MQ-135 感測器
analog_pin = machine.ADC(0)
digital_pin = machine.Pin(16, machine.Pin.IN)

# 設定 DHT11 感測器
dht_sensor = dht.DHT11(machine.Pin(2))

def read_sensor():
    digital_status = digital_pin.value()
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    hum = dht_sensor.humidity()
    return digital_status, temp, hum

def draw_large_text(oled, text, x, y):
    for i, char in enumerate(text):
        oled.text(char, x + i*8, y)
        oled.text(char, x + i*8, y + 8)

def display_sensor_data():
    while True:
        digital_status, temp, hum = read_sensor()
        oled.fill(0)
        
        # 簡化顯示資訊
        air_quality_status = "AIR G" if not digital_status else "AIR B"
        display_text = '{} {}C H{}%'.format(air_quality_status, temp, hum)
        
        # 顯示數據
        draw_large_text(oled, display_text, 0, 24)
        oled.show()
        time.sleep(5)  # 每 5 秒更新一次

display_sensor_data()
