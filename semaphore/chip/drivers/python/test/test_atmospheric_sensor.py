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

from grid_io.bme280 import BME280


def test_atmospheric_sensor():

    sensor = BME280(2, address=0x77, mode=BME280.modes.ULTRALOWPOWER)

    degrees = sensor.read_temperature()
    hectopascals = sensor.read_pressure() / 100
    humidity = sensor.read_humidity()

    print('Timestamp = {0:0.3f}'.format(sensor.t_fine))
    print('Temp      = {0:0.3f} deg C'.format(degrees))
    print('Pressure  = {0:0.2f} hPa'.format(hectopascals))
    print('Humidity  = {0:0.2f} %'.format(humidity))
