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
I2C driver for the Adafruit LED Matrix with backpack.

    https://www.adafruit.com/products/1614
"""

from .ht16k33 import HT16K33, is_bit


class Matrix8x8(HT16K33):
    """
    Adafruit 8x8 LED matrix with backpack.

    The user can wire very different 8x8 LED matrix in many different ways to
    the HT16K33. This class implements the specific transformations between
    "visual" rows and columns to HT16K33's "memory" rows and columns required
    to match wiring for Adafruit's backpacks for 8x8 LED matrix.
    """

    @property
    def rows(self):
        return 8

    @property
    def columns(self):
        return 8

    def __init__(self, busnum, address):
        super().__init__(busnum, address)

    def _visual_to_memory(self, row, column):
        assert 0 <= row < self.rows
        assert 0 <= column < self.columns

        led = ((row + 7) % 8) + column * 16
        mrow = led // 8
        mcolumn = led % 8
        print(
            'Led: {}, Row: {}, Col: {}'.format(led, mrow, mcolumn)
        )
        return (mrow, mcolumn)

    def write_bitmap(self, bitmap):
        assert len(bitmap) == self.rows
        for row in bitmap:
            assert len(row) == self.columns
            assert all(map(is_bit, row))

        # Copy bitmap
        for row in range(self.rows):
            for column in range(self.columns):
                self[row, column] = bitmap[row][column]

    def __getitem__(self, key):
        return super()[self._visual_to_memory(*key)]

    def __setitem__(self, key, value):
        super()[self._visual_to_memory(*key)] = value

    def __iter__(self):
        for row in range(self.rows):
            for column in range(self.columns):
                yield row, column

    def __str__(self):
        output = []
        for row in range(self.rows):
            output.append(' '.join([
                str(self[row, column])
                for column in range(self.columns)
            ]))
        return '\n'.join(output)


__all__ = ['Matrix8x8']
