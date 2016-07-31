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
I2C base class for drivers.
"""


class DummySMBus(object):
    """
    Dummy wrapper for the SMBus object that log the I2C writes.
    """
    def __init__(self, busid):
        self._busid = busid

    def write_byte(self, addr, val):
        print('[{}] 0x{:X} = b{:08b}'.format(
            self._busid, addr, val
        ))


class I2CDevice(object):
    """
    Base class for I2C devices.

    :var uint address: Assigned I2C address.
    :var uint8 busid: Assigned IC2 bus identifier.

    :param uint address: I2C address.
    :param uint8 busid: IC2 bus identifier.
    :param bool dummy: Use a dummy I2C writer for debugging instead of real
     I2C writes.
    """
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
        """
        Write given byte command to the device address.

        :param uint8 cmd: Byte command to send to the device.
        """
        self._bus.write_byte(self._address, (cmd & 0xFF))


__all__ = ['I2CDevice']