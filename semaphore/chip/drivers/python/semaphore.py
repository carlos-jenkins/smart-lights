#!/usr/bin/env python3

from grid_io.semaphore import Semaphore

URI = 'http://hwthoncr16.herokuapp.com/thegrid'

if __name__ == '__main__':
    s = Semaphore(URI)
    s.start()
