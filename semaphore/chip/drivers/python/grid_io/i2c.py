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

import logging


def bound_bits(value, bits):
    return 0 <= value <= 2 ** 8 - 1


class I2CDevice(object):
    """
    Class for communicating with an I2C device.

    Allows reading and writing 8-bit, 16-bit, and byte array values to
    registers on the device.

    It can handle signed, unsigned and endianness.

    :var uint address: Assigned I2C address.
    :var uint8 busid: Assigned IC2 bus identifier.

    :param uint address: I2C address.
    :param uint busid: IC2 bus identifier.
    :param class i2c_class: Class implementing the I2C reading interface.
     If None, smbus.SMBus will be used.
    """

    def __init__(self, busnum, address, i2c_class=None):
        self._busnum = busnum
        self._address = address

        if i2c_class is None:
            from smbus import SMBus
            self._bus = SMBus(busnum)
        else:
            self._bus = i2c_class(busnum)

        self._logger = logging.getLogger(
            '/dev/i2c-{}/{:#x}'.format(busnum, address)
        )

    def _debug(self):
        self._logger.setLevel(logging.DEBUG)
        self._logger.addHandler(logging.StreamHandler())

    @property
    def busnum(self):
        return self._busnum

    @property
    def address(self):
        return self._address

    def write(self, value):
        """
        Write the specified 8-bit value to the device base address.
        """
        assert bound_bits(value, 8)

        self._bus.write_byte(self._address, value)
        self._logger.debug(
            'Wrote value {:#x}'.format(value)
        )

    def register_write_u8(self, register, value):
        """
        Write an 8-bit value to the specified 8-bit register.
        """
        assert bound_bits(register, 8)
        assert bound_bits(value, 8)

        self._bus.write_byte_data(self._address, register, value)
        self._logger.debug(
            'Wrote to register {:#x} value {:#x}'.format(register, value)
        )

    def register_write_u16(self, register, value):
        assert bound_bits(register, 8)
        assert bound_bits(value, 16)

        self._bus.write_word_data(self._address, register, value)
        self._logger.debug(
            'Wrote to register pair {:#x}, {:#x} value {:#x} '.format(
                register, register + 1, value
            )
        )

    def read(self):
        """
        Read the device base address and return a 8-bit value.
        """
        result = self._bus.read_byte(self._address) & 0xFF
        self._logger.debug(
            'Read value {:#x}'.format(result)
        )
        return result

    def register_read_u8(self, register):
        """
        Read the specified 8-bit register and return a 8-bit value.
        """
        assert bound_bits(register, 8)

        result = self._bus.read_byte_data(self._address, register) & 0xFF
        self._logger.debug(
            'Read from register {:#x} returns {:#x}'.format(register, result)
        )

        return result

    def register_read_s8(self, register):
        """
        Read the specified 8-bit register and return a signed 7-bit value.
        """
        result = self.register_read_u8(register)
        if result > 127:
            result -= 256
            self._logger.debug('... as signed: {:#x}'.format(result))
        return result

    def register_read_u16(self, register, little_endian=True):
        """
        Read the specified 8-bit register and return a 16-bit value with the
        specified endianness.

        Default is little endian, or least significant byte first.
        """
        assert bound_bits(register, 8)

        result = self._bus.read_word_data(self._address, register) & 0xFFFF
        self._logger.debug(
            'Read from register pair {:#x}, {:#x} value {:#x} '.format(
                register, register + 1, result
            )
        )

        # Swap bytes if using big endian because read_word_data assumes little
        # endian on ARM (little endian) systems.
        if not little_endian:
            result = ((result << 8) & 0xFF00) + (result >> 8)
            self._logger.debug('... as big endian: {:#x}'.format(result))
        return result

    def register_read_s16(self, register, little_endian=True):
        """
        Read the specified 8-bit register and return a signed 15-bit value
        with the specified endianness.

        Default is little endian, or least significant byte first.
        """
        result = self.register_read_u16(register, little_endian)
        if result > 32767:
            result -= 65536
            self._logger.debug('... as signed: {:#x}'.format(result))
        return result

    def register_read_u16le(self, register):
        """
        Same as register_read_u16 with endianness set to little endian.
        """
        return self.register_read_u16(register, little_endian=True)

    def register_read_u16be(self, register):
        """
        Same as register_read_u16 with endianness set to big endian.
        """
        return self.register_read_u16(register, little_endian=False)

    def register_read_s16le(self, register):
        """
        Same as register_read_s16 with endianness set to little endian.
        """
        return self.register_read_s16(register, little_endian=True)

    def register_read_s16be(self, register):
        """
        Same as register_read_s16 with endianness set to big endian.
        """
        return self.register_read_s16(register, little_endian=False)


__all__ = ['I2CDevice']
