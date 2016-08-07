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

from grid_io.trinket import Trinket


def test_trinket_read_sensor():

    sensor = Trinket(2, 18)

    noise = sensor.read_audio()
    gas = sensor.read_gas();

    print('Noise = {0}:{0:016b} dB'.format(noise))
    print('Gas  = {0}:{0:016b} '.format(gas))

def test_trinket_transmitter():

    sensor = Trinket(2, 18)

    write_semaphore_state(True)
    write_semaphore_state(False)
