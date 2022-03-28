import requests
import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import random

from scipy import rand
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False


def get_electic_data():
    url = 'https://data.taipower.com.tw/opendata/apply/file/d006005/台灣電力公司_過去電力供需資訊.csv'
    r = requests.get(url, allow_redirects=True)
    open('./本年度每日尖峰備轉容量率.csv', 'wb').write(r.content)


def get_electic_data_day():
    url = '	https://data.taipower.com.tw/opendata/apply/file/d006002/本年度每日尖峰備轉容量率.csv'
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
# （系統運轉淨尖峰供電能力－系統瞬時尖峰負載(瞬間值)）÷系統瞬時尖峰負載(瞬間值)×100%
# (x-y) =備轉容量 => (備轉容量 / y) *100= 備轉容量率


def calculate_electric_serve(start_day=6):
    data = pd.read_csv("./Data/本年度每日尖峰備轉容量率.csv",
                       encoding='utf-8', dtype=object)
    date = list(map(lambda x: x.replace('/', ''),  data['日期'].tolist()))
    # 備轉容量to (MW)
    md = list(map(lambda x: int(float(x)*10), data['備轉容量(萬瓩)'].tolist()))
    ww = list(map(lambda x: float(x),  data['備轉容量率(%)'].tolist()))
    ee = []  # 轉淨尖峰供電能力
    dd = []  # 尖峰負載
    for index in range(len(ww)):
        d = md[index]*100 / ww[index]
        dd.append(int(d))
        ee.append(int(d+md[index]))

    day = start_day  # 20220101為星期六
    with open('./Data/本年度每日尖峰備轉容量率整理.csv', 'w', encoding='UTF8', newline='') as f:
        header = ['日期', '星期', '淨尖峰供電能力(MW)',
                  '尖峰負載(MW)', '備轉容量(MW)', '備轉容量率(%)']
        writer = csv.writer(f)
        writer.writerow(header)
        for index in range(len(ww)):
            writer.writerow([date[index], day, ee[index],
                            dd[index], md[index], ww[index]])
            day += 1
            if day > 7:
                day = 1


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
            [item['淨尖峰供電能力(MW)'], item['尖峰負載(MW)'], item['備轉容量(MW)'], item['日期'], item['日期'][4:-2]])
    header = ['淨尖峰供電能力(MW)', '尖峰負載(MW)', '備轉容量(MW)', '日期', '月份']
    for i in date_key:
        with open('./Data/台灣電力公司_過去電力供需整理星期{}資訊.csv'.format(i), 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for data in stage_list[i]:
                writer.writerow(data)


def last_year_data(date, kind="備轉容量(MW)", csv="./Data/台灣電力公司_過去電力供需整理資訊.csv"):
    data = pd.read_csv(csv,
                       encoding='utf-8', dtype=object)
    for i in range(len(data)):
        item = data.loc[i]
        if item['日期'] == '2021'+date[-4:]:
            return int(item[kind])
    return int(3000)


def predict_recent(data):
    dd_part = {"1": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7": []}
    ee_part = {"1": [], "2": [], "3": [], "4": [], "5": [], "6": [], "7": []}
    # 起首0沒有作用，純粹補位
    latest_week = {"dd": [0, 0, 0, 0, 0, 0, 0, 0],
                   "ee": [0, 0, 0, 0, 0, 0, 0, 0]}
    fc = data['日期'].tolist()
    day = data['星期'].tolist()
    ee = data['尖峰負載(MW)'].tolist()
    dd = data['淨尖峰供電能力(MW)'].tolist()
    for i in range(len(fc)):
        latest_week["dd"][int(day[i])] = int(dd[i])
        latest_week["ee"][int(day[i])] = int(ee[i])
        ee_part[day[i]].append(int(ee[i]))
        dd_part[day[i]].append(int(dd[i]))
    return latest_week, ee_part, dd_part


# 利用去年資料作為粗估的溫度預測 # 簡單預測淨尖峰供電能力
def dd_predict(dd_part, latest_dd, day, date):
    tmp_dd = 0
    for i in dd_part[day]:
        tmp_dd += int(i)
    tmp_dd /= len(dd_part[day])
    predict=int((int(latest_dd[int(day)])*0.8+tmp_dd*0.15+last_year_data(date, kind='淨尖峰供電能力(MW)')*0.05))
   
    if in_holiday(date):
        if day in ["6", "7"]:
            predict = (predict+ random.randint(35000,36000))/2   
        else:
            predict = (predict+ random.randint(28000,33000))/2   
    else:
        if day in ["6", "7"]:
             predict =  (predict+ random.randint(28000,29000))/2   
        else:
            predict =  (predict+ random.randint(33000,35000))/2   
    return predict


def ee_predict(ee_part, latest_ee, day, date):
    tmp_ee = 0
    predict = 0
    for i in ee_part[day]:
        tmp_ee += int(i)
    tmp_ee /= len(ee_part[day])
    if in_holiday(date):
        if day in ["6", "7"]:
            predict = int(latest_ee[int(day)]*0.8+tmp_ee *0.2)+random.randint(-1200, 1200)
            
        else:
            predict = int(latest_ee[int(day)]*0.9+tmp_ee *0.1)+random.randint(-350, 350)
    else:
        predict = int(int(latest_ee[int(day)])*0.9+tmp_ee*0.08 + last_year_data(date, kind='尖峰負載(MW)')*0.02)
    return predict


def in_holiday(date):
    return date in ['20220402', '20220403', '20220404', '20220405']


def plot_data(kind='備轉容量(MW)'):
    for day in range(7):
        data = pd.read_csv(
            "./Data/台灣電力公司_過去電力供需整理星期{}資訊.csv".format(day+1), encoding='utf-8', dtype=object)
        # ee = list(map(int, data['淨尖峰供電能力(MW)'].tolist()))
        print("./Data/台灣電力公司_過去電力供需整理星期{}資訊.csv".format(day+1))
        dd = list(map(int, data[kind].tolist()))
        # plt.plot([*range(len(ee))], ee, label="淨尖峰供電能力")
        plt.plot([*range(len(dd))], dd, label="星期{}{}".format(day+1, kind))
    plt.legend()
    plt.show()


def plot_recent(kind='備轉容量(MW)'):
    week = {}
    data = pd.read_csv("./Data/本年度每日尖峰備轉容量率整理.csv",
                       encoding='utf-8', dtype=object)
    day = data['星期'].tolist()
    ee = data[kind].tolist()
    for index in range(len(day)):
        if day[index] not in week:
            week[day[index]] = [int(ee[index])]
        else:
            week[day[index]].append(int(ee[index]))
    for i in range(7):
        plt.plot([*range(len(week[str(i+1)]))],  week[str(i+1)],
                 label="星期{}{}".format(i+1, kind))
    plt.legend()
    plt.show()


def simple_predict(day):
    if day in [6, 7]:
        return random.randint(-250, 250)
    else:
        return random.randint(-100, 450)


# modify_highpeak_eachday()
# split_to_date_stage()
# plot_recent()
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
    import pandas as pd
    # df_training = pd.read_csv(args.training)
    # model = Model()
    # model.train(df_training)
    # df_result = model.predict(n_step=7)
    # df_result.to_csv(args.output, index=0)
    header = ['date', 'operating_reserve(MW)']
    date_list = [{"date": '20220330', "day": '3'},
                 {"date": '20220331', "day": '4'},
                 {"date": '20220401', "day": '5'},
                 {"date": '20220402', "day": '6'},
                 {"date": '20220403', "day": '7'},
                 {"date": '20220404', "day": '1'},
                 {"date": '20220405', "day": '2'},
                 {"date": '20220406', "day": '3'},
                 {"date": '20220407', "day": '4'},
                 {"date": '20220408', "day": '5'},
                 {"date": '20220409', "day": '6'},
                 {"date": '20220410', "day": '7'},
                 {"date": '20220411', "day": '1'},
                 {"date": '20220412', "day": '2'},
                 {"date": '20220413', "day": '3'},
                 ]
    data = pd.read_csv("./Data/本年度每日尖峰備轉容量率整理.csv",
                       encoding='utf-8', dtype=object)
    # latest_week:讀取最新一周狀況
    # ee_part:將所有尖峰供電能力分成星期
    # ee_part:將所有尖峰負載分成星期
    # holiday:放假節日
    latest_week, ee_part, dd_part = predict_recent(data)

    with open(args.output, 'w', encoding='UTF8', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(header)
        for date in date_list:
            tmp = []
            tmp.append(date['date'])
            ff = dd_predict(dd_part, latest_week['dd'], date['day'], date['date'])-ee_predict(ee_part, latest_week['ee'], date['day'], date['date'])
            if 2400> ff or ff>4500:
                
                ff=last_year_data(date['date'])+random.randint(-250,500)
            # else:
            #     ff=(ff+random.randint(3100,3500))/2
            tmp.append(int(ff))
            # print(tmp)
            writer.writerow(tmp)
            # write a row to the csv file
