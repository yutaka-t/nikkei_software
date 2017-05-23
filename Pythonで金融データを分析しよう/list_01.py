import datetime
import requests
import pandas as pd
from datetime import datetime, date
import zipfile


def __gaincap_datetime_parser(str_dt):
    try:
        return datetime.strptime(str_dt[:-3], '%Y-%m-%d %H:%M:%S.%f')
    except Exception:
        return datetime.strptime(str_dt, '%Y-%m-%d %H:%M:%S')


def download_gaincap(filename, path):
    tsdflg = True
    url_gc_path = "http://ratedata.gaincapital.com/"

    for i in range(len(filename)):
        # ファイル取得
        url_file_path = filename[i]
        url_date_path = "2017/01 January/"
        url = url_gc_path + url_date_path + url_file_path
        res = requests.get(url)

        # ファイルの保存
        hd_path = path + url_file_path

        # f = open(hd_path, 'wb')
        # f.write(res.content)
        # f.close()

        with open(hd_path, 'wb') as f:
            f.write(res.content)

        # zipファイルからの読み込み
        file_csv = "USD_JPY_Week%d.csv" %(i+1)
        try:
            f = zipfile.ZipFile(hd_path).open(file_csv)
            dfx = pd.read_csv(f, index_col=3, date_parser=__gaincap_datetime_parser)[['RateBid']]
            f.close()
            if tsdflg:
                tsd = dfx.copy()
                tsdflg = False
            else:
                tsd = tsd.append(dfx)
        except Exception:
            print("Error open zip file %s. The error is" %filename[i])
    return tsd

if __name__ == '__main__':
    filename0 = ["USD_JPY_Week1.zip",
                 "USD_JPY_Week2.zip",
                 "USD_JPY_Week3.zip",
                 "USD_JPY_Week4.zip",
                 "USD_JPY_Week5.zip"]
    path0 = "./data"
    ts = download_gaincap(filename0, path0)

    print("end--------------------------------------", len(ts))





