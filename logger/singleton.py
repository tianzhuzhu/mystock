import logging
import os
import sys
import threading
import time
import traceback
from functools import wraps




def Singleton(cls):
    instances = {}
    def _singleton(*args,**kwargs):
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return _singleton






