
from turtle import color
from pytest import console_main
import requests
from fake_useragent import UserAgent
import pandas as pd
from bs4 import BeautifulSoup as BS
import csv
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
plt.rcParams['axes.unicode_minus'] = False
def get_electic_data():
    url = 'https://data.taipower.com.tw/opendata/apply/file/d006005/台灣電力公司_過去電力供需資訊.csv'
    r = requests.get(url, allow_redirects=True)
    open('./本年度每日尖峰備轉容量率.csv', 'wb').write(r.content)


def modify_data():
    data = pd.read_csv("./Data/台灣電力公司_過去電力供需資訊.csv", encoding='utf-8')
    fc = data['日期'].tolist()
    ee = data['淨尖峰供電能力(MW)'].tolist()
    dd = data['尖峰負載(MW)'].tolist()
    ff = data['備轉容量(MW)'].tolist()
    qq = data['備轉容量率(%)'].tolist()
    header = ['日期', '淨尖峰供電能力(MW)', '尖峰負載(MW)', '備轉容量(MW)', '備轉容量率(%)', '星期']
    first = 6
    with open('./Data/台灣電力公司_過去電力供需整理資訊.csv', 'w', encoding='UTF8', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(header)
        for i in range(len(fc)):
            tmp = [fc[i], ee[i], dd[i], ff[i], qq[i], first]
            first += 1
            if first > 7:
                first = 1
            writer.writerow(tmp)


def split_to_date_stage():
    data = pd.read_csv("./Data/台灣電力公司_過去電力供需整理資訊.csv",
                       encoding='utf-8', dtype=object)
    stage_list = {}
    date_key = ['1', '2', '3', '4', '5', '6', '7']
    for i in range(7):
        stage_list[str(i+1)] = []
    for i in range(len(data)):
        item = data.loc[i]
        stage_list[item['星期']].append(
            [item['淨尖峰供電能力(MW)'], item['尖峰負載(MW)'], item['備轉容量(MW)'],item['日期'],item['日期'][4:-2]])
    header = ['淨尖峰供電能力(MW)', '尖峰負載(MW)', '備轉容量(MW)','日期','月份']
    for i in date_key:
        with open('./Data/台灣電力公司_過去電力供需整理星期{}資訊.csv'.format(i), 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for data in stage_list[i]:
                writer.writerow(data)

def predict_test(date):
    data = pd.read_csv("./Data/台灣電力公司_過去電力供需整理資訊.csv",
                       encoding='utf-8', dtype=object)
    for i in range(len(data)):
        item = data.loc[i]
        if item['日期'] == date:
            return   item['備轉容量(MW)']  
    return "3000"

def plot_data(day=1):
    data = pd.read_csv("./Data/台灣電力公司_過去電力供需整理星期{}資訊.csv".format(day), encoding='utf-8', dtype=object)
    ee = list(map(int, data['淨尖峰供電能力(MW)'].tolist()))
    dd = list(map(int, data['尖峰負載(MW)'].tolist()))
    test =list(map(lambda x: x[4:-2],  data['日期']))
    print(test)
    plt.plot([*range(len(ee))],ee , label = "淨尖峰供電能力")
    plt.plot( [*range(len(dd))],dd, label = "尖峰負載",color='red')
    plt.legend()
    plt.show()
# split_to_date_stage()
# plot_data()
# You can write code above the if-main block.
if __name__ == '__main__':
    # You should not modify this part, but additional arguments are allowed.
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--training',
                        default='training_data.csv',
                        help='input training data file name')

    parser.add_argument('--output',
                        default='submission.csv',
                        help='output file name')
    args = parser.parse_args()

    # The following part is an example.
    # You can modify it at will.
    # import pandas as pd
    # df_training = pd.read_csv(args.training)
    # model = Model()
    # model.train(df_training)
    # df_result = model.predict(n_step=7)
    # df_result.to_csv(args.output, index=0)
    import csv
    header = ['date', 'operating_reserve(MW)']
    date_list = [{"date": '20220330', "day": 3},
                 {"date": '20220331', "day": 4},
                 {"date": '20220401', "day": 5},
                 {"date": '20220402', "day": 6},
                 {"date": '20220403', "day": 7},
                 {"date": '20220404', "day": 1},
                 {"date": '20220405', "day": 2},
                 {"date": '20220406', "day": 3},
                 {"date": '20220407', "day": 4},
                 {"date": '20220408', "day": 5},
                 {"date": '20220409', "day": 6},
                 {"date": '20220410', "day": 7},
                 {"date": '20220411', "day": 1},
                 {"date": '20220412', "day": 2},
                 {"date": '20220413', "day": 3},
                 ]
    
    with open(args.output, 'w', encoding='UTF8', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(header)
        for date in date_list:
            tmp = []
            # print('2021'+date['date'][-4:])
            # print(predict_test('2021'+date['date'][-4:]))
            # print(date)
            tmp.append(date['date'])
            tmp.append(int(predict_test('2021'+date['date'][-4:]))+250)
            # print(tmp)
            writer.writerow(tmp)
            # write a row to the csv file
