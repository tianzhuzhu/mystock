import os
import sys
import traceback

import yaml
print(sys.path[0] )

def loadData(name):
    try:
        dirname, filename = os.path.split(os.path.abspath(__file__))
        # print(dirname)
        cur_path=dirname
        file=os.path.join(cur_path, name)
        print(file)
        file = open(file, 'r', encoding="utf-8")

        file_data = file.read()
        data = yaml.load(file_data, Loader=yaml.FullLoader)
    except:
        traceback.print_exc()
    return data



# database:
#     engine: mysql+pymysql://root:root@localhost:3306/njmat
#     username: root
#     password: root
#     driver: pymysql
#     database: njmat
#     port: 3306
#     host: 127.0.0.1
#     db: njmat
#     charset: utf8