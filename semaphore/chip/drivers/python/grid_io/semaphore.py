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

from .bme280 import BME280
from .trinket import Trinket
from .matrix8x8 import Matrix8x8


class Semaphore(object):

    def __init__(self):
        self._busnum = 2

        self._green = Matrix8x8(self._busnum, 0x70)
        self._yellow = Matrix8x8(self._busnum, 0x71)
        self._red = Matrix8x8(self._busnum, 0x74)
        self._trinket = Trinket(self._busnum, 0x12)
        self._bme280 = BME280(
            self._busnum,
            address=0x77,
            mode=BME280.modes.ULTRALOWPOWER
        )

        self._state = None
        self.set_semaphore(False)

    def gather_data(self):
        data = {}
        data['gas'] = self._trinket.read_gas()
        data['audio'] = self._trinket.read_audio()
        data['temperature'] = self._bme280.read_temperature()
        data['pressure'] = self._bme280.read_pressure()
        data['humidity'] = self._bme280.read_humidity()
        return data

    def set_semaphore(self, state):
        if state == self._state:
            return

        if state:
            self._red.clear()
            self._red.flush()

            self._green.fill(True)
            self._green.flush()

            self._trinket.write_semaphore_state(True)
            self._state = True

        else:
            self._green.fill(True)
            self._green.flush()
            self._green.set_blink_rate(Matrix8x8.BLINK_HALFHZ)
            sleep(3)
            self._green.clear()
            self._green.flush()
            self._green.set_blink_rate(Matrix8x8.BLINK_OFF)

            self._yellow.fill(True)
            self._yellow.flush()
            sleep(2)
            self._yellow.clear()
            self._yellow.flush()

            self._green.fill(True)
            self._green.flush()

            self._trinket.write_semaphore_state(False)
            self._state = False


__all__ = ['Semaphore']