from os import listdir
from pandas import read_csv
# _______________________________________________________________________________


def Load_Files(dir):
    data = {}
    entries = listdir(dir)
    titles = ['Sensor', 'TimeStamp', 'Roll', 'Pitch', 'Yaw', 'xGyr', 'yGyr', 'zGyr',
              'BatteryLVL']
    for i in entries:
        if 'SENSOR' in i:
            name = i.split('.')
            s = read_csv(dir + i, sep=",")
            s.columns = titles
            s['TimeStamp'] = s['TimeStamp']/1000
            data[name[0]] = s
    return data
