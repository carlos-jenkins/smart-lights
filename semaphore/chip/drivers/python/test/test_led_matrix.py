from time import sleep
from grid_io.ht16k33 import LEDMatrix8x8, HT16K33


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


def test_ladder():

    m = HT16K33(2, 0x74)

    for r in range(m.rows):
        for c in range(m.columns):
            m[r, c] = 1
            m.flush()
            sleep(1)
            m.clear()
