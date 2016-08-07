from time import sleep
from grid_io.semaphore import Semaphore


def test_transition():

    print('Semaphore is default RED')
    semaphore = Semaphore()

    sleep(5)
    print('Semaphore is going GREEN')
    semaphore.set_semaphore(True)

    print('Semaphore is going RED')
    sleep(5)
    semaphore.set_semaphore(False)

    print('Semaphore is going GREEN')
    sleep(5)
    semaphore.set_semaphore(True)

    print('Semaphore is going RED')
    sleep(5)
    semaphore.set_semaphore(False)

def test_send_data():
    semaphore = Semaphore('http://hwthoncr16.herokuapp.com/thegrid')
    while True:
        semaphore.send_data()
