
from pytest import console_main
import requests
from fake_useragent import UserAgent
user_agent = UserAgent()
headers = {'Usesr-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
           "Content-Type": "application/json;charset=UTF-8"}

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
            print(date)
            tmp.append(date['date'])
            tmp.append("2455")
            print(tmp)
            writer.writerow(tmp)
            # write a row to the csv file
