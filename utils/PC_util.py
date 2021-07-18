import ctypes
import os


# 获取计算机名
def getname()->str:
    pcName = ctypes.c_char_p(''.encode('utf-8'))
    pcSize = 16
    pcName = ctypes.cast(pcName, ctypes.c_char_p)
    try:
        ctypes.windll.kernel32.GetComputerNameA(pcName, ctypes.byref(ctypes.c_int(pcSize)))
    except Exception:
        print("Sth wrong in getname!")
    return pcName.value.decode('utf-8')

def main():
    getname()

if __name__ == "__main__":
    main()
