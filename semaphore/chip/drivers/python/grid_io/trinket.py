from .i2c import I2CDevice
from argparse import Namespace

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
        audio = (a << 8) | b;
        print audio
        return audio


    def read_gas(self):
        """
        Reads the gas levels from sensor plugged into Trinket.
        """
        self.write(Trinket._registers.GAS)
        a = self.read()
        b = self.read()
        gas = (a << 8) | b;
        print gas
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
