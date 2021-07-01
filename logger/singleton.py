import logging
import os
import sys
import threading
import time
import traceback
from functools import wraps

import my_logger


def singleton(cls):
    instances = {}
    def _singleton(*args,**kwargs):
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return _singleton

if __name__ == "__main__":
    my_logger.a()
    my_logger.b()





