from .bme280 import BME280, BME280_OSAMPLE_8


def test_atmospheric_sensor():

    sensor = BME280(2, 0x77, mode=BME280_OSAMPLE_8)

    degrees = sensor.read_temperature()
    hectopascals = sensor.read_pressure() / 100
    humidity = sensor.read_humidity()

    print('Timestamp = {0:0.3f}'.format(sensor.t_fine))
    print('Temp      = {0:0.3f} deg C'.format(degrees))
    print('Pressure  = {0:0.2f} hPa'.format(hectopascals))
    print('Humidity  = {0:0.2f} %'.format(humidity))
