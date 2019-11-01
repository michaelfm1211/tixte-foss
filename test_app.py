from tixte_foss import app
from multiprocessing import Process
import pytest


def test_run():
    server = Process(target=app.run)
    server.start()
    server.terminate()
