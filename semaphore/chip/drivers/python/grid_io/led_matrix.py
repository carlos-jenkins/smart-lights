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

from numpy import zeros

from .i2c import I2CDevice


class HT16K33(I2CDevice):

    BLINK_OFF = 0
    BLINK_2HZ = 1
    BLINK_1HZ = 2
    BLINK_HALFHZ = 3

    _BLINK_DISPLAYON = 0x01

    _CMD_BLINK = 0x80
    _CMD_BRIGHTNESS = 0xE0
    _CMD_OSCILLATOR_ON = 0x21

    _MEM_ROWS = 8
    _MEM_COLS = 16

    @property
    def rows(self):
        return self._rows

    @property
    def columns(self):
        return self._columns

    def __init__(self, busid, address, rows=None, columns=None, dummy=False):
        super().__init__(busid, address, dummy=dummy)

        self._display_buffer = zeros((HT16K33._MEM_ROWS), dtype='uint16')

        if rows is None:
            rows = HT16K33._MEM_ROWS
        if columns is None:
            columns = HT16K33._MEM_COLS

        self._rows = rows
        self._columns = columns

        # Chip initialization routine
        self._i2c_command(HT16K33._CMD_OSCILLATOR_ON)
        self.set_blink_rate(HT16K33.BLINK_OFF)
        self.set_brightness(15)

    def set_brightness(self, value):
        assert 0 <= value <= 15

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
            HT16K33._CMD_BLINK | HT16K33._BLINK_DISPLAYON | (value << 1)
        )

    def flush(self):
        # Start at address 0x00
        self._i2c_command(0x00)
        for row in self._display_buffer:
            self._i2c_command(row & 0xFF)
            self._i2c_command(row >> 8)

    def clear(self):
        self._display_buffer.fill(0)

    def write_bitmap(self, bitmap):

        # Check bitmap consistency
        def is_bit(e):
            return e in [0, 1, False, True]
        assert len(bitmap) == self._rows
        for row in bitmap:
            assert len(row) == self._columns
            assert all(map(is_bit, row))

        # Copy bitmap
        for row in self._rows:
            for column in self._columns:
                self[row, column] = bitmap[row][column]

    def __getitem__(self, key):
        row, column = key
        assert 0 <= row < self._rows
        assert 0 <= column < self._columns

        bit = (self._display_buffer[row] >> column) & 0x1
        return bit

    def __setitem__(self, key, value):
        row, column = key

        # Support for boolean value set
        if value is True:
            value = 1
        elif value is False:
            value = 0

        assert 0 <= row < self._rows
        assert 0 <= column < self._columns
        assert value in [0, 1]

        # Clear bit
        if value == 0:
            self._display_buffer[row] &= (~(0x1 << column) & 0xFFFF)
        # Set bit
        else:
            self._display_buffer[row] |= 0x1 << column

    def __delitem__(self, key):
        raise RuntimeError('Cannot delete bits')

    def __iter__(self):
        for row in self._rows:
            for column in self._columns:
                yield row, column, self[row][column]

    def __repr__(self):
        return str(self)

    def __str__(self):
        output = []
        for row in self._display_buffer:
            output.append(
                ' '.join(reversed(list(
                    '{{:0{}b}}'.format(self._columns).format(row)
                )))
            )
        return '\n'.join(output)


class LEDMatrix(HT16K33):
    def __init__(self, busid, address, dummy=False):
        super().__init__(busid, address, rows=8, columns=8, dummy=dummy)


__all__ = ['LEDMatrix']
