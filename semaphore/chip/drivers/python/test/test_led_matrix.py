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

from time import sleep
from grid_io.matrix8x8 import Matrix8x8


def test_bitmap():

    m = Matrix8x8(2, 0x74)
    m.clear()
    m.flush()
    bitmap = [
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0],
    ]
    m.write_bitmap(bitmap)
    m.flush()
    sleep(4)
    m.clear()
    m.flush()


def test_ladder():

    m = Matrix8x8(2, 0x74)

    for r in range(m.rows):
        for c in range(m.columns):
            m[r, c] = 1
            m.flush()
            sleep(1)
            m.clear()

    m.flush()


def test_flash():

    m = Matrix8x8(2, 0x74)

    m.fill(1)
    m.flush()
    m.set_blink_rate(m.BLINK_2HZ)
    m.set_brightness(1)
    sleep(5)
    m.set_blink_rate(m.BLINK_1HZ)
    m.set_brightness(15)
    sleep(5)
    m.set_blink_rate(m.BLINK_OFF)
    m.clear()
    m.flush()
