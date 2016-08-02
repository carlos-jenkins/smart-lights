# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Carlos Jenkins
# Copyright (C) 2016 Carolina Aguilar
# Copyright (c) 2014 Adafruit Industries
#
# Based on Adafruit_BME280.py by Tony DiCola, based on the BMP280 driver with
# BME280 changes provided by David J Taylor, Edinburgh (www.satsignal.eu)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from time import sleep
from argparse import Namespace

from .i2c import I2CDevice


class BME280(I2CDevice):
    """
    Python I2C driver for the BME280 temperature, humidity and pressure sensor
    by Bosch.

    Tested with Adafruit breakout board:

        https://www.adafruit.com/products/2652

    By default, the I2C address is 0x77.
    If you add a jumper from SDO to GND, the address will change to 0x76.
    """

    _registers = Namespace(**{
        'DIG_T1': 0x88,  # Trimming parameter registers
        'DIG_T2': 0x8A,
        'DIG_T3': 0x8C,

        'DIG_P1': 0x8E,
        'DIG_P2': 0x90,
        'DIG_P3': 0x92,
        'DIG_P4': 0x94,
        'DIG_P5': 0x96,
        'DIG_P6': 0x98,
        'DIG_P7': 0x9A,
        'DIG_P8': 0x9C,
        'DIG_P9': 0x9E,

        'DIG_H1': 0xA1,
        'DIG_H2': 0xE1,
        'DIG_H3': 0xE3,
        'DIG_H4': 0xE4,
        'DIG_H5': 0xE5,
        'DIG_H6': 0xE6,
        'DIG_H7': 0xE7,

        'CHIPID': 0xD0,
        'VERSION': 0xD1,
        'SOFTRESET': 0xE0,

        'CONTROL_HUM': 0xF2,
        'CONTROL': 0xF4,
        'CONFIG': 0xF5,
        'PRESSURE_DATA': 0xF7,
        'TEMP_DATA': 0xFA,
        'HUMIDITY_DATA': 0xFD
    })

    modes = Namespace(**{
        'ULTRALOWPOWER': 1,       # Oversampling 1
        'LOWPOWER': 2,            # Oversampling 2
        'STANDARD': 3,            # Oversampling 4
        'HIGHRESOLUTION': 4,      # Oversampling 8
        'ULTRAHIGHRESOLUTION': 5  # Oversampling 16
    })

    def __init__(
            self, busnum, address=0x77,
            mode=modes.ULTRALOWPOWER,
            **kwargs):

        super().__init__(busnum, address)

        # Check that mode is valid.
        if mode not in vars(BME280.modes).values():
            raise ValueError(
                'Unexpected mode value {0}. '
                'Set mode to one of {}'.format(
                    ', '.join([
                        'BME280.modes.{}'.format(key)
                        for key in BME280.modes.keys()
                    ])
                )
            )
        self._mode = mode

        # Load calibration values.
        self._load_calibration()

        # Initial known setting: 0xF3 0b00111111
        #
        # Bit 7, 6, 5 osrs_t[2:0] Controls oversampling of temperature data.
        #     001 -> oversampling ×1. See table 22 in datasheet.
        # Bit 4, 3, 2 osrs_p[2:0] Controls oversampling of pressure data.
        #     111 -> oversampling ×16. See table 22 in datasheet.
        # Bit 1, 0 mode[1:0] Controls the power mode of the device.
        #     11 -> Normal mode. See table 10.
        self.register_write_u8(BME280._registers.CONTROL, 0x3F)
        self.t_fine = 0.0

    def _load_calibration(self):

        self._dig_t1 = self.register_read_u16le(BME280._registers.DIG_T1)
        self._dig_t2 = self.register_read_s16le(BME280._registers.DIG_T2)
        self._dig_t3 = self.register_read_s16le(BME280._registers.DIG_T3)

        self._dig_p1 = self.register_read_u16le(BME280._registers.DIG_P1)
        self._dig_p2 = self.register_read_s16le(BME280._registers.DIG_P2)
        self._dig_p3 = self.register_read_s16le(BME280._registers.DIG_P3)
        self._dig_p4 = self.register_read_s16le(BME280._registers.DIG_P4)
        self._dig_p5 = self.register_read_s16le(BME280._registers.DIG_P5)
        self._dig_p6 = self.register_read_s16le(BME280._registers.DIG_P6)
        self._dig_p7 = self.register_read_s16le(BME280._registers.DIG_P7)
        self._dig_p8 = self.register_read_s16le(BME280._registers.DIG_P8)
        self._dig_p9 = self.register_read_s16le(BME280._registers.DIG_P9)

        self._dig_h1 = self.register_read_u8(BME280._registers.DIG_H1)
        self._dig_h2 = self.register_read_s16le(BME280._registers.DIG_H2)
        self._dig_h3 = self.register_read_u8(BME280._registers.DIG_H3)
        self._dig_h6 = self.register_read_s8(BME280._registers.DIG_H7)

        h4 = self.register_read_s8(BME280._registers.DIG_H4)
        h4 = (h4 << 24) >> 20
        self._dig_h4 = h4 | (
            self.register_read_u8(BME280._registers.DIG_H5) & 0x0F
        )

        h5 = self.register_read_s8(BME280._registers.DIG_H6)
        h5 = (h5 << 24) >> 20
        self._dig_h5 = h5 | (
            self.register_read_u8(BME280._registers.DIG_H5) >> 4 & 0x0F
        )

    def _read_raw_temperature(self):
        """
        Reads the raw (uncompensated) temperature from the sensor.
        """
        meas = self._mode
        self.register_write_u8(BME280._registers.CONTROL_HUM, meas)

        meas = self._mode << 5 | self._mode << 2 | 1
        self.register_write_u8(BME280._registers.CONTROL, meas)

        # Wait the required time
        sleep_time = 0.00125 + 0.0023 * (1 << self._mode)
        sleep_time = sleep_time + 0.0023 * (1 << self._mode) + 0.000575
        sleep_time = sleep_time + 0.0023 * (1 << self._mode) + 0.000575
        sleep(sleep_time)

        msb = self.register_read_u8(BME280._registers.TEMP_DATA)
        lsb = self.register_read_u8(BME280._registers.TEMP_DATA + 1)
        xlsb = self.register_read_u8(BME280._registers.TEMP_DATA + 2)
        raw = ((msb << 16) | (lsb << 8) | xlsb) >> 4
        return raw

    def _read_raw_pressure(self):
        """
        Reads the raw (uncompensated) pressure level from the sensor.

        Assumes that the temperature has already been read.
        Which means that enough delay has been provided.
        """
        msb = self.register_read_u8(BME280._registers.PRESSURE_DATA)
        lsb = self.register_read_u8(BME280._registers.PRESSURE_DATA + 1)
        xlsb = self.register_read_u8(BME280._registers.PRESSURE_DATA + 2)
        raw = ((msb << 16) | (lsb << 8) | xlsb) >> 4
        return raw

    def _read_raw_humidity(self):
        """
        Reads the raw (uncompensated) humidity from the sensor.

        Assumes that the temperature has already been read.
        Which means that enough delay has been provided.
        """
        msb = self.register_read_u8(BME280._registers.HUMIDITY_DATA)
        lsb = self.register_read_u8(BME280._registers.HUMIDITY_DATA + 1)
        raw = (msb << 8) | lsb
        return raw

    def read_temperature(self):
        """
        Gets the compensated temperature in degrees celsius.
        """
        # float in Python is double precision
        uncompensated = float(self._read_raw_temperature())
        var1 = (
            (uncompensated / 16384.0 - self._dig_t1 / 1024.0) *
            float(self._dig_t2)
        )
        var2 = (
            (uncompensated / 131072.0 - self._dig_t1 / 8192.0) *
            (uncompensated / 131072.0 - self._dig_t1 / 8192.0) *
            float(self._dig_t3)
        )
        self.t_fine = int(var1 + var2)
        temp = (var1 + var2) / 5120.0
        return temp

    def read_pressure(self):
        """
        Gets the compensated pressure in Pascals.
        """
        adc = self._read_raw_pressure()
        var1 = self.t_fine / 2.0 - 64000.0
        var2 = var1 * var1 * self._dig_p6 / 32768.0
        var2 = var2 + var1 * self._dig_p5 * 2.0
        var2 = var2 / 4.0 + self._dig_p4 * 65536.0
        var1 = (
            self._dig_p3 * var1 * var1 / 524288.0 + self._dig_p2 * var1
        ) / 524288.0
        var1 = (1.0 + var1 / 32768.0) * self._dig_p1

        if var1 == 0:
            return 0

        p = 1048576.0 - adc
        p = ((p - var2 / 4096.0) * 6250.0) / var1
        var1 = self._dig_p9 * p * p / 2147483648.0
        var2 = p * self._dig_p8 / 32768.0
        p = p + (var1 + var2 + self._dig_p7) / 16.0

        return p

    def read_humidity(self):
        """
        Gets the compensated humidity in percent (0.0-100.0).
        """
        adc = self._read_raw_humidity()
        h = self.t_fine - 76800.0
        h = (
            (adc - (self._dig_h4 * 64.0 + self._dig_h5 / 16384.8 * h)) *
            (
                self._dig_h2 / 65536.0 *
                (
                    1.0 + self._dig_h6 / 67108864.0 * h * (
                        1.0 + self._dig_h3 / 67108864.0 * h
                    )
                )
            )
        )
        h = h * (1.0 - self._dig_h1 * h / 524288.0)

        # Set boundary
        h = min(h, 100.0)
        h = max(h, 0.0)

        return h


__all__ = ['BME280']
