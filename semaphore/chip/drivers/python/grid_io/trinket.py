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

from argparse import Namespace
from .i2c import I2CDevice


class Trinket(I2CDevice):

    _registers = Namespace(**{
        'AUDIO': ord('A'),
        'GAS': ord('G'),
        'CONTINUE': ord('C'),
        'STOP': ord('S')
    })

    def __init__(self, busnum, address):
        super().__init__(busnum, address)

    def read_audio(self):
        """
        Reads the audio from mic plugged into Trinket.
        """
        self.write(Trinket._registers.AUDIO)
        a = self.read()
        b = self.read()
        audio = (a << 8) | b
        return audio

    def read_gas(self):
        """
        Reads the gas levels from sensor plugged into Trinket.
        """
        self.write(Trinket._registers.GAS)
        a = self.read()
        b = self.read()
        gas = (a << 8) | b
        return gas

    def write_semaphore_state(self, state):
        """
        Sends a value for the transmitter to transmit.
        """
        if state:
            self.write(Trinket._registers.CONTINUE)
        else:
            self.write(Trinket._registers.STOP)


__all__ = ['Trinket']
