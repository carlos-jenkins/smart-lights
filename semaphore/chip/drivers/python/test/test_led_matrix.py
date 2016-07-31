from time import sleep
from grid_io.ht16k33 import LEDMatrix8x8


def test_matrix():

    m = LEDMatrix8x8(2, 0x74)
    sleep(4)
    m.clear()
    m.flush()
    sleep(4)

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
