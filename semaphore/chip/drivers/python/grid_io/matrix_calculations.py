def set_pixel(x, y, value):
    led = y * 16 + ((x + 7) % 8)
    print(
        'LED: {}, Value: {}'.format(led, value)
    )
    pos = led // 8
    offset = led % 8
    print(
        'Row (pos): {}, Col (offset): {}'.format(pos, offset)
    )
