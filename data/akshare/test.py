import ctypes
import os
import akshare as ak
stock_em_yjyg_df = ak.stock_em_yjyg(date="20210630")
print(stock_em_yjyg_df)

# 获取计算机名
def getname():
    pcName = ctypes.c_char_p(''.encode('utf-8'))
    pcSize = 16
    pcName = ctypes.cast(pcName, ctypes.c_char_p)
    try:
        ctypes.windll.kernel32.GetComputerNameA(pcName, ctypes.byref(ctypes.c_int(pcSize)))
    except Exception:
        print("Sth wrong in getname!")
    print(pcName.value.decode('utf-8'))


def main():
    getname()


if __name__ == "__main__":
    main()
    