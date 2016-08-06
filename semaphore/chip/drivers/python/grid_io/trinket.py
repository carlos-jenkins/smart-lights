from .i2c import I2CDevice


class Trinket(I2CDevice):

    _registers = Namespace(**{
        'AUDIO': ord('A'),
        'GAS': ord('G')
    })

    def __init__(self, busnum, address):
        super().__init__(busnum, address)

    def read_audio(self):
        """
        Reads the audio from mic plugged into Trinket.
        """
        audio = self.register_read_u16(Trinket._registers.AUDIO)
        return audio


    def read_gas(self):
        """
        Reads the gas levels from sensor plugged into Trinket.
        """
        gas = self.register_read_u16(Trinket._registers.GAS)
        return gas

    def write_transmitter(self, state):
        """
        Sends a value for the transmitter to transmit.
        """
        self.register_write_u8(Trinket._registers.TRINKET, state)


__all__ = ['Trinket']
