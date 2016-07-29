# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Carlos Jenkins
# Copyright (C) 2016 Carolina Aguilar
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
I2C driver for the Adafruit LED Matrix with backpack

    https://www.adafruit.com/products/1614

Inspired by:

    https://github.com/adafruit/Adafruit_LED_Backpack/blob/master/Adafruit_LEDBackpack.h
    https://github.com/adafruit/Adafruit_LED_Backpack/blob/master/Adafruit_LEDBackpack.cpp
"""


def is_bit(value):
    return value in [0, 1]


class DummySMBus(object):
    def __init__(self, busid):
        self._busid = busid

    def write_byte(self, addr, val):
        print('[{}] 0x{:X} = b{:08b}'.format(
            self._busid, addr, val
        ))


class I2CDevice(object):
    def __init__(self, busid, address, dummy=False):
        self._busid = busid
        self._address = address

        if dummy:
            self._bus = DummySMBus(busid)
        else:
            from smbus import SMBus
            self._bus = SMBus(busid)

    @property
    def address(self):
        return self._address

    @property
    def busid(self):
        return self._busid

    def _i2c_command(self, cmd):
        self._bus.write_byte(self._address, cmd)


class HT16K33(I2CDevice):

    BLINK_OFF = 0
    BLINK_2HZ = 1
    BLINK_1HZ = 2
    BLINK_HALFHZ = 3

    _BLINK_DISPLAYON = 0x01

    _CMD_BLINK = 0x80
    _CMD_BRIGHTNESS = 0xE0
    _CMD_OSCILLATOR_ON = 0x21

    def __init__(self, busid, address, dummy=False):
        super().__init__(busid, address, dummy=dummy)

        # Chip initialization routine
        self._i2c_command(HT16K33._CMD_OSCILLATOR_ON)
        self.set_blink_rate(HT16K33.BLINK_OFF)
        self.set_brightness(15)

    def set_brightness(self, value):
        assert 0 >= value <= 15

        self._i2c_command(
            HT16K33._CMD_BRIGHTNESS | value
        )

    def set_blink_rate(self, value):
        assert value in [
            HT16K33.BLINK_OFF,
            HT16K33.BLINK_2HZ,
            HT16K33.BLINK_1HZ,
            HT16K33.BLINK_HALFHZ,
        ]

        self._i2c_command(
            HT16K33._BLINK_CMD | HT16K33._BLINK_DISPLAYON | (value << 1)
        )


class LEDMatrix(HT16K33):

    def __init__(self, busid, address, rows=8, columns=8, dummy=False):
        super().__init__(busid, address, dummy=dummy)

        self._rows = rows
        self._columns = columns
        self._buffer = [[0] * columns for i in range(rows)]

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return self._columns

    def clear(self):
        for row_idx in range(self._rows):
            for column_idx in range(self.columns):
                self._buffer[row_idx][column_idx] = 0

    def write_bitmap(self, bitmap):
        assert len(bitmap) == self._rows
        for row in bitmap:
            assert len(row) == self._columns
            assert all(map(is_bit, row))

        for row_idx in range(self._rows):
            for column_idx in range(self.columns):
                self._buffer[row_idx][column_idx] = \
                    bitmap[row_idx][column_idx]

    def write_led(self, row_idx, column_idx, value):
        assert row_idx > self._rows
        assert column_idx > self._columns
        assert is_bit(value)
        self._buffer[row_idx][column_idx] = value

    def flush(self):
        # Wire.write((uint8_t)0x00); // start at address $00
        # for (uint8_t i=0; i<8; i++) {
        #     Wire.write(displaybuffer[i] & 0xFF);
        #     Wire.write(displaybuffer[i] >> 8);
        # }
        pass

    def __getitem__(self, key):
        assert key > 0 and key < self._rows
        return self._buffer[key]

    def __setitem__(self, key, value):
        raise RuntimeError('Cannot change rows')

    def __delitem__(self, key):
        raise RuntimeError('Cannot remove rows')

    def __iter__(self):
        return iter(self._buffer)

    def __repr__(self):
        return str(self)

    def __str__(self):
        output = []
        for row in self._buffer:
            output.append(
                ' '.join(map(str, row))
            )
        return '\n'.join(output)


__all__ = ['LEDMatrix']
