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
from threading import Thread
from datetime import datetime

from flask import Flask
from requests import post

from .bme280 import BME280
from .trinket import Trinket
from .matrix8x8 import Matrix8x8


external_state = False
server = Flask('SmartLight')


@server.route('/state/<int:state>')
def external_state_set(state):
    global external_state
    external_state = state == 0
    return ''


class Semaphore(object):

    def __init__(self, uri, semaphore_id=1):
        self._busnum = 2
        self._semaphore_id = semaphore_id

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
        self.set_semaphore(external_state)

        self.uri = uri

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
            self._green.set_blink_rate(Matrix8x8.BLINK_2HZ)
            sleep(3)
            self._green.clear()
            self._green.flush()
            self._green.set_blink_rate(Matrix8x8.BLINK_OFF)

            self._yellow.fill(True)
            self._yellow.flush()
            sleep(2)
            self._yellow.clear()
            self._yellow.flush()

            self._red.fill(True)
            self._red.flush()

            self._trinket.write_semaphore_state(False)
            self._state = False

    def send_data(self):
        semaphore_data = {}
        semaphore_data['id_semaphore'] = self._semaphore_id
        semaphore_data['timestamp'] = datetime.now().isoformat()
        semaphore_data['state'] = self._state
        semaphore_data.update(self.gather_data())
        post(self.uri, data=semaphore_data)
        print(semaphore_data)

    def start(self, host='0.0.0.0', port=8080):

        def server_start():
            global server
            server.run(host=host, port=port, debug=False)

        server_thread = Thread(target=server_start)
        server_thread.start()

        while True:
            global external_state
            self.set_semaphore(external_state)
            print('Semaphore is set to: {}'.format(external_state))
            self.send_data()


__all__ = ['Semaphore']
