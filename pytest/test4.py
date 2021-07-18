import win32clipboard
import re
import time

def clipboard_get():
    """获取剪贴板数据"""
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return data


def clipboard_set(data):
    """设置剪贴板数据"""
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, data)
    win32clipboard.CloseClipboard()


# 初始化替换字符列表，相比于正则使用replace函数进行单字符替换更快
char_list = [('（', '('),
             ('）', ')'),
             ('“', '"'),
             ('”', '"'),
             ('‘', '\''),
             ('’', '\''),
             ('print ', 'print '),
             ('？','?'),
             ('。','.'),
             (' ','.'),
             ('，',','),
             ]

# 预编译正则替换匹配表达式
# 匹配python2格式的 print函数文本
sub_print = re.compile(r'\bprint\s+(.+)')
# 匹配csdn复制自带的版权声明后缀文本
sub_csdn = re.compile(r'—+\s+版权声明：本文为CSDN.*\s+原文链接.*')


# 指定场景 sub替换函数：python2格式的 print函数 替换为python3格式
def sub_fn(s):
    return 'print(' + s.group(1).strip() + ')\r\n'


# 判断如果没有要替换的字符则返回None，有则执行替换操作，先进行字符列表replace，再执行reg.sub(sub_fn, txt)
def char_replace_reg_sub(txt):
    new_txt = txt

    # 对字符列表中字符 逐一判断，如果字符在文本中 则replace替换，如果都不在 则return None，不用再进行替换操作
    i = 0
    for old_char, new_char in char_list:
        if old_char in new_txt:
            i += 1
            new_txt = new_txt.replace(old_char, new_char)
    if i == 0:
        return None

    print('-' * 150, '\n【After char replace】:', new_txt)
    # 对指定场景替换 使用正则re.sub
    new_txt = sub_print.sub(sub_fn, new_txt)
    new_txt = sub_csdn.sub('', new_txt)
    print('【After sub replace:】', new_txt)
    return new_txt


def main():
    """后台脚本：每隔0.2秒，读取剪切板文本，检查有无指定字符或字符串，如果有则执行替换"""
    # recent_txt 存放最近一次剪切板文本，初始化值只多执行一次paste函数读取和替换
    recent_txt = clipboard_get()
    replaced_txt = char_replace_reg_sub(recent_txt)
    clipboard_set(recent_txt if replaced_txt is None else replaced_txt)

    while True:
        # txt 存放当前剪切板文本
        txt = clipboard_get()

        # 剪切板内容和上一次对比如有变动，再进行内容判断，判断后如果发现有指定字符在其中的话，再执行替换
        if txt != recent_txt:
            # print(f'txt:{txt}')
            new_txt = char_replace_reg_sub(txt)  # 没查到要替换的子串，返回None

            if new_txt is not None:
                clipboard_set(new_txt)
                # 更新 recent_txt 为替换之后的文本，便于下次与 txt 剪切板文本对比，判断内容有无更新
                recent_txt = new_txt

        # 检测间隔（延迟0.2秒）
        time.sleep(0.2)


if __name__ == '__main__':
    main()