import inspect
import logging
import os
import sys
import threading
import time
import traceback
from functools import wraps
from inspect import getargvalues, stack

from logger.singleton import Singleton

@Singleton
class Logger():
    def __init__(self,logfile=None):
        self.logger = logging.getLogger()
        formater = logging.Formatter('%(asctime)s %(name)s  %(levelname)s   %(lineno)d '
                                     '%(thread)d %(threadName)s %(process)d %(message)s')
        if logfile == None:
            cur_path = os.path.split(os.path.realpath(__file__))[0]
            stime = time.strftime("%Y-%m-%d",time.localtime())
            logfile = cur_path + os.sep + "log_" + stime + ".log"
        else:
            logfile = logfile
        self.sh = logging.StreamHandler(sys.stdout)
        self.sh.setFormatter(formater)
        self.fh = logging.FileHandler(logfile)
        self.fh.setFormatter(formater)
        self.logger.addHandler(self.sh)
        self.logger.addHandler(self.fh)
        self.logger.setLevel(logging.INFO)
def get_class_from_frame(fr):
    args, _, _, value_dict = getargvalues(fr)
    if len(args) and args[0] == 'self':
        instance = value_dict.get('self', None)
        if instance:
            return getattr(instance, '__class__', None)
    return None

def  logit(description=''):
    lg=Logger()
    lg=lg.logger
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            path=os.path.abspath(inspect.getfile(func))
            if(description==''):
                try:
                    lg.info(path+' '+func.__name__+' start')
                    res=func(*args, **kwargs)
                    lg.info(path+' '+func.__name__+' finshed')
                except:
                    err_str = traceback.format_exc()
                    lg.error(path+' '+func.__name__+' error')
                    lg.error(err_str)
                else:
                    return res
            else:
                try:
                    lg.info(description+' start')
                    res=func(*args, **kwargs)
                    lg.info(description+' finshed')
                except:
                    err_str = traceback.format_exc()
                    lg.error(description+' error')
                    lg.error(err_str)
                else:
                    return res
        return wrapped_function
    return logging_decorator
@logit()
def a(a=1,b=2):
    return a+b
@logit()
def b():
    b=1/0
a(a=1,b=2)
