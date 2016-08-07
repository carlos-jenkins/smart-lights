from time import sleep
from grid_io.semaphore import Semaphore


def test_transition():

    semaphore = Semaphore()

    semaphore.set_semaphore(True)
    sleep(5)
    semaphore.set_semaphore(False)
    sleep(5)
    semaphore.set_semaphore(True)
    sleep(5)
    semaphore.set_semaphore(False)
