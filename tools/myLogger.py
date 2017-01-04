import os
import logging
import sys
import psutil


def set_My_Logger(log_FilePath):
    logger = logging.getLogger()
    fh=logging.FileHandler(log_FilePath)
    ch=logging.StreamHandler(stream=sys.stdout)
    formatter =logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(fh)
    logger.addHandler(ch)
    pid = psutil.Process(os.getpid())
    print_Mem_Occupy = lambda: logger.info(
        "系统内存情况：" + str(psutil.virtual_memory()) + '程序内存情况：' + str(pid.memory_info()))
    return logger,print_Mem_Occupy